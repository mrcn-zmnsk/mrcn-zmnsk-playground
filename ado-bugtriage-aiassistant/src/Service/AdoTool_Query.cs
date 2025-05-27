namespace TriageApp.Server.Service
{
    using System.Text.Json;
    using OpenAI.Chat;

    public class AdoTool_Query : IChatTool
    {
        IAdoFacade adoFacade;

        public AdoTool_Query(IAdoFacade adoFacade)
        {
            this.adoFacade = adoFacade;
        }

        public ChatTool ChatTool
        {
            get
            {
                return ChatTool.CreateFunctionTool
                (
                    functionName: "query_ado",
                    functionDescription: "gets results of an Azure DevOps query with a given query id",
                    functionParameters: BinaryData.FromString(this.ParametersSchema)
                );
            }
        }

        public async Task<string> CallTool(ChatToolCall toolCall)
        {
            var arguments = JsonDocument.Parse(toolCall.FunctionArguments);
            if (arguments.RootElement.TryGetProperty("queryId", out var queryId))
            {
                return await this.adoFacade.RunQuery(queryId.GetGuid());
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
                            QueryId = new
                            {
                                Type = "string",
                                Format = "uuid",
                                Description = "Query ID of the query stored in Azure Devops"
                            }
                        },
                        Required = new[] { "queryId" },
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
