namespace TriageApp.Server.Service
{
    using System.Text.Json;
    using OpenAI.Chat;

    public class AdoTool_GetDetails : IChatTool
    {
        IAdoFacade adoFacade;

        public AdoTool_GetDetails(IAdoFacade adoFacade)
        {
            this.adoFacade = adoFacade;
        }
               
        public ChatTool ChatTool
        {
            get
            {
                return ChatTool.CreateFunctionTool
                (
                    functionName: "fetch_bug",
                    functionDescription: "fetches a bug from Azure DevOps",
                    functionParameters: BinaryData.FromString(this.ParametersSchema)
                );
            }
        }

        public async Task<string> CallTool(ChatToolCall toolCall)
        {
            var arguments = JsonDocument.Parse(toolCall.FunctionArguments);

            if (arguments.RootElement.TryGetProperty("workItemId", out var workItemId))
            {
                var fetchedItem = await adoFacade.GetADOItem(workItemId.GetInt32());
                var docxSteps = await adoFacade.GetReproFromDocx(workItemId.GetInt32());

                return @$"
#Work Item  {workItemId.GetInt32()} 

##Content
{fetchedItem}

## Additional repro steps document
{docxSteps}";
            }

            return "The tool could not process the request because workItemId argument was not provided";
        }

        internal string ParametersSchema
        {
            get
            {
                return JsonSerializer.Serialize
                (
                    new
                    {
                        Type = "object",
                        Properties = new
                        {
                            WorkItemId = new
                            {
                                Type = "integer",
                                Description = "ID of the Azure dev ops work item"
                            }
                        },
                        Required = new[] { "workItemId" },
                    },
                    new JsonSerializerOptions
                    {
                        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                        WriteIndented = true,
                    }
                );
            }
        }
    }
}
