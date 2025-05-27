namespace TriageApp.Server.Service
{
    using OpenAI.Chat;
    using System.Collections.Generic;
    using System.Threading.Tasks;

    public interface IAdoTriageAssistant
    {
        Task<IList<ChatMessage>> Init();
        Task<IList<ChatMessage>> ProcessMessages(IList<ChatMessage> messages);
    }
}