using System.Text.Json.Serialization;

namespace PrintagoManager.Models
{
    public class BambuAuthRequest
    {
        [JsonPropertyName("username")] // The Bambu API often uses 'username' for the email field
        public string Email { get; set; } = "";

        [JsonPropertyName("password")]
        public string Password { get; set; } = "";
    }
}
