namespace TriageApp.Server.Service
{
    using OpenAI.Chat;
    using System.Threading.Tasks;

    public interface IChatTool
    {
        ChatTool ChatTool { get; }

        Task<string> CallTool(ChatToolCall toolCall);
    }
}