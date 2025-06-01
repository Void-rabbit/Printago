// Models/PartialSkuInsert.cs
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace PrintagoManager.Models
{
    public class PartialSkuInsert
    {
        [JsonPropertyName("title")]
        public string? Title { get; set; }

        [JsonPropertyName("description")]
        public string? Description {get; set;}

        // For updating linkedParts, the API might expect a full replacement or support partial updates.
        // If full replacement, it would be:
        // [JsonPropertyName("linkedParts")]
        // public List<LinkedPartInsert>? LinkedParts { get; set; }

        // Add other updatable fields from PartialSkuInsert schema
        // e.g., folderId
        // [JsonPropertyName("folderId")] public string? FolderId {get; set;}
    }
}
