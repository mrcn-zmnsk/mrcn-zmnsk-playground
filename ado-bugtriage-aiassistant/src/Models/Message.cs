namespace TriageApp.Server.Models
{
    using System.ComponentModel.DataAnnotations;

    public class Message
    {
        public string Author { get; set; }
        
        [Required]
        public string Text { get; set; }        
    }
}
