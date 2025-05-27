namespace TriageApp.Server.Controllers
{
    using Microsoft.AspNetCore.Mvc;
    using Microsoft.Extensions.Caching.Memory;
    using OpenAI.Chat;
    using TriageApp.Server.Models;
    using TriageApp.Server.Service;

    [ApiController]
    [Route("[controller]")]
    public class AdoTriageController : ControllerBase
    {
        const string SESSIONKEY = "asdfdsfs";

        IMemoryCache cache;
        IAdoTriageAssistant adoTriageAssistant;

        public AdoTriageController(IMemoryCache cache, IAdoTriageAssistant adoTriageAssistant)
        {
            this.cache = cache;
            this.adoTriageAssistant = adoTriageAssistant;
        }

        [HttpGet]
        public async Task<IActionResult> Get()
        {
            var messageHistory = await this.adoTriageAssistant.Init();
            messageHistory = await this.adoTriageAssistant.ProcessMessages(messageHistory);
            
            var response = messageHistory
                .Where(_ => _.GetType() == typeof(AssistantChatMessage) && _.Content.Count > 0)
                .Select(_ => new Message { Author = _.GetType().Name, Text = _.Content[0].Text }).ToList();

            this.cache.Set(SESSIONKEY, messageHistory);
            return Ok(response);
        }

        [HttpPost]
        public async Task<IActionResult> Post(Message message)
        {
            if (this.cache.TryGetValue<IList<ChatMessage>>(SESSIONKEY, out var messageHistory))
            {
                messageHistory.Add( ChatMessage.CreateUserMessage(message.Text));

                messageHistory = await this.adoTriageAssistant.ProcessMessages(messageHistory);
                var lastMessage = messageHistory.Last();

                var response = new Message { Text = lastMessage.Content[0].Text, Author = lastMessage.GetType().Name };

                this.cache.Set(SESSIONKEY, messageHistory);
                return Ok(response);
            }

            throw new Exception();
        }
    }
}
