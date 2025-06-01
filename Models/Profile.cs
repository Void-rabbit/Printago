// Models/Profile.cs
using System;
using System.Text.Json.Serialization;

namespace PrintagoManager.Models
{
    public class Profile
    {
        [JsonPropertyName("id")]
        public string? Id { get; set; }

        [JsonPropertyName("name")]
        public string? Name { get; set; }

        [JsonPropertyName("type")]
        public string? Type { get; set; } // "process", "filament", "machine"

        [JsonPropertyName("source")]
        public string? Source { get; set; } // "manual", "bambu-account"

        // Data is a complex object, potentially Dictionary<string, object> or specific class
        // [JsonPropertyName("data")]
        // public Dictionary<string, object>? Data { get; set; }

        [JsonPropertyName("createdAt")]
        public DateTime CreatedAt { get; set; }
        // Add other relevant properties
    }
}
