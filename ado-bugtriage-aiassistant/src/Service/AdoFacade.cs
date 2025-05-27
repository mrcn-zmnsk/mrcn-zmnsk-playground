namespace TriageApp.Server.Service
{
    using Azure.Identity;
    using DocumentFormat.OpenXml.Packaging;
    using Microsoft.TeamFoundation.WorkItemTracking.WebApi;
    using Microsoft.TeamFoundation.WorkItemTracking.WebApi.Models;
    using Microsoft.VisualStudio.Services.Client;
    using Microsoft.VisualStudio.Services.Common;
    using Microsoft.VisualStudio.Services.WebApi;
    using Newtonsoft.Json;

    public class AdoFacade : IAdoFacade
    {
        WorkItemTrackingHttpClient wit;
        string project;

        public AdoFacade(string orgUrl, string project, string pat = "")
        {
            this.project = project;

            var connection = string.IsNullOrEmpty(pat) ?
                new VssConnection(new Uri(orgUrl), new VssAzureIdentityCredential(new DefaultAzureCredential())) :
                new VssConnection(new Uri(orgUrl), new VssBasicCredential(string.Empty, pat));

            wit = connection.GetClient<WorkItemTrackingHttpClient>();
        }

        public async Task<string> GetADOItem(int itemId)
        {
            var fieldSelection = new string[]
            {
                "System.Title",
                "System.Description",
                "System.Tags",
                "Microsoft.VSTS.TCM.ReproSteps",
                "Microsoft.VSTS.Common.Issue",
                "Microsoft.VSTS.CMMI.HowFound",
                "Microsoft.Dynamics.CompliantInPrivacy",
                "Microsoft.Dynamics.CompliantInSecurity",
                "Microsoft.Dynamics.CompliantInAccessibility",
                "Microsoft.Dynamics.SecurityRating",
                "Microsoft.Dynamics.Partner",
                "Microsoft.Dynamics.Customer",
                "Microsoft.Dynamics.OpenVersion",
            };
            var item = await this.wit.GetWorkItemAsync(this.project, itemId, fieldSelection);

            var response = new Dictionary<string, object>();

            response.AddRange(item.Fields.Select(_ => new KeyValuePair<string, object>(_.Key.Split('.').Last(), _.Value)));

            response.Add("workItemId", item.Id);
            var link = item.Links.Links["html"] as ReferenceLink;
            response.Add("url", link?.Href);

            return JsonConvert.SerializeObject(response);
        }

        public async Task<string> GetReproFromDocx(int itemId)
        {
            string response = "";

            try
            {
                var item = await this.wit.GetWorkItemAsync(this.project, itemId, expand: WorkItemExpand.Relations);

                foreach (var attachment in item.Relations.Where(_ => _.Rel == "AttachedFile"))
                {
                    if (attachment.Attributes.TryGetValue<string>("name", out var name))
                    {
                        if (name.EndsWith("docx", StringComparison.OrdinalIgnoreCase))
                        {
                            var content = await this.wit.GetAttachmentContentAsync(new Guid(attachment.Url.Split('/').Last()));

                            using (var wordDoc = WordprocessingDocument.Open(content, false))
                            {
                                response = wordDoc.MainDocumentPart.Document.Body.InnerText;
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Covering exception: {ex.Message}");
            }

            return response;
        }

        public async Task<string> RunQuery(Guid queryId)
        {
            var results = await this.wit.QueryByIdAsync(this.project, queryId);

            return JsonConvert.SerializeObject(results);
        }
    }
}
