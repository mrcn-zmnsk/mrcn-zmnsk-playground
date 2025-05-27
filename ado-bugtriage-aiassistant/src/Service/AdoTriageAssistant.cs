namespace TriageApp.Server.Service
{
    using Azure.AI.OpenAI;
    using Azure.Identity;
    using Microsoft.VisualStudio.Services.Common;
    using OpenAI.Chat;

    public class AdoTriageAssistant : IAdoTriageAssistant
    {
        ChatClient chatClient;

        ChatCompletionOptions options;

        IChatTool[] tools;
        IConfiguration configuration;
        ILogger<AdoTriageAssistant> logger;

        public AdoTriageAssistant(IAdoFacade adoFacade, IConfiguration configuration, ILogger<AdoTriageAssistant> logger)
        {
            this.tools = new IChatTool[] { new AdoTool_GetDetails(adoFacade), new AdoTool_Query(adoFacade) };
            this.configuration = configuration;
            this.logger = logger;

            this.chatClient = new AzureOpenAIClient(new Uri(configuration["openAiClient:endpointUrl"]), new DefaultAzureCredential()).GetChatClient(configuration["openAiClient:modelDeployment"]);
            this.options = new ChatCompletionOptions();
            this.options.Tools.AddRange(this.tools.Select(t => t.ChatTool));
        }

        public async Task<IList<ChatMessage>> Init()
        {
            return new List<ChatMessage>
            {
                 ChatMessage.CreateSystemMessage($@"
You are an assistant to an engineering team doing a bug triage. 
You should start by executing triage query and fetch the list of bugs. For each bug in the query result: 
 - fetch bug details
 - summarize it 
 - determine what ERP scenario it is about
 - determine if the bug states a version in which the scenario worked, prior to the version in which the bug is opened
 - determine if the bug speaks about blockage or existing workaround. summarize the workaround if available.
 - determine if the customer wants it backported to a previous release or not. this is the basis for priority assessment.
 - assign priority and severity according to the triage defintions

Sort the results in ascending severity order. Present the results in markdown format. Include a link to ADO for each bug.
"
                 ),
                 ChatMessage.CreateSystemMessage($"Unless specified by the user the triage queryId is {this.configuration["ado:triageQueryId"]}"),
                 ChatMessage.CreateSystemMessage(@$"
The triage defintions are below. Bug reports often over-emphasize severity of the issue. Be strict in applying the guidelines and don't take severity suggestions from the bug into consideration: 
{await LoadTriageDefinition()}"),
            };
        }

        public async Task<IList<ChatMessage>> ProcessMessages(IList<ChatMessage> messages)
        {
            int attempts = 10;
            while (--attempts >= 0)
            {
                if (messages.Last() is AssistantChatMessage)
                {
                    return messages;
                }

                var chatCompletion = (await chatClient.CompleteChatAsync(messages, this.options)).Value;

                switch (chatCompletion.FinishReason)
                {
                    case ChatFinishReason.ToolCalls:
                        await HandleToolCall(messages, chatCompletion);
                        break;
                    default:
                        HandleTextResponse(messages, chatCompletion);
                        break;
                }

                this.logger.LogInformation("Input tokens: {0}, output tokens: {1}", chatCompletion.Usage.InputTokenCount, chatCompletion.Usage.OutputTokenCount);
            }

            return messages;
        }

        internal void HandleTextResponse(IList<ChatMessage> messages, ChatCompletion chatCompletion)
        {
            var textResponse = chatCompletion.Content[0].Text;
            this.logger.LogInformation("Triage Assistant: {0}", textResponse);
            messages.Add(ChatMessage.CreateAssistantMessage(textResponse));
        }

        internal async Task HandleToolCall(IList<ChatMessage> messages, ChatCompletion chatCompletion)
        {
            messages.Add(ChatMessage.CreateAssistantMessage(chatCompletion));
            foreach (var toolCall in chatCompletion.ToolCalls)
            {
                this.logger.LogInformation($"Triage Assistant: Calling tool: {toolCall.FunctionName} with arguments: {toolCall.FunctionArguments}");

                var tool = this.tools.Single(_ => _.ChatTool.FunctionName == toolCall.FunctionName);

                var toolResponse = await tool.CallTool(toolCall);

                this.logger.LogInformation($"Triage Assistant: Tool response: {toolResponse}");
                messages.Add(ChatMessage.CreateToolMessage(toolCall.Id, toolResponse));
            }
            return;
        }

        internal async Task<string> LoadTriageDefinition()
        {
            return await File.ReadAllTextAsync("triage-policy.md");
        }
    }
}
