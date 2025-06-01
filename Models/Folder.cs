// Models/Folder.cs
using System.Text.Json.Serialization;

namespace PrintagoManager.Models
{
    public class Folder
    {
        [JsonPropertyName("id")]
        public string? Id { get; set; }

        [JsonPropertyName("name")]
        public string? Name { get; set; }

        [JsonPropertyName("type")]
        public string? Type { get; set; } // "part" or "sku"

        [JsonPropertyName("parentId")]
        public string? ParentId { get; set; }

        // Add other properties from the Folder schema if present in OpenAPI spec
        // e.g., storeId, createdAt, updatedAt
    }
}
