using System.Text.Json.Serialization; // Required for JsonPropertyName if used

namespace PrintagoManager.Models
{
    public class Part
    {
        [JsonPropertyName("id")]
        public string? Id { get; set; }

        [JsonPropertyName("name")]
        public string? Name { get; set; }

        [JsonPropertyName("type")]
        public string? Type { get; set; } // e.g., "stl", "3mf"

        [JsonPropertyName("description")]
        public string? Description { get; set; }

        [JsonPropertyName("fileUris")]
        public List<string>? FileUris { get; set; }

        [JsonPropertyName("storeId")]
        public string? StoreId { get; set; }

        [JsonPropertyName("createdAt")]
        public DateTime CreatedAt { get; set; }

        [JsonPropertyName("updatedAt")]
        public DateTime UpdatedAt { get; set; }

        // Add other relevant properties from OpenAPI spec for Part schema later
    }
}
