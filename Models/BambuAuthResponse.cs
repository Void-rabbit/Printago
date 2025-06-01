using System.Text.Json.Serialization;

namespace PrintagoManager.Models
{
    public class BambuAuthResponse
    {
        [JsonPropertyName("access_token")]
        public string? AccessToken { get; set; }

        [JsonPropertyName("refresh_token")]
        public string? RefreshToken { get; set; }

        [JsonPropertyName("user_id")]
        public string? UserId { get; set; }

        [JsonPropertyName("name")] // Often included with user info
        public string? UserName { get; set; }

        [JsonPropertyName("email")]
        public string? Email {get; set; }

        [JsonPropertyName("expires_in")]
        public int ExpiresIn { get; set; } // Seconds until expiry

        // Placeholder for other potential fields returned on login that might be useful
        // [JsonPropertyName("some_other_field")]
        // public string? SomeOtherField { get; set; }
    }
}
