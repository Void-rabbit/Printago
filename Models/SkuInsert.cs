// Models/SkuInsert.cs
using System.Collections.Generic;
using System.Text.Json.Serialization;
using System.ComponentModel.DataAnnotations;

namespace PrintagoManager.Models
{
    public class LinkedPartInsert
    {
        [Required]
        [JsonPropertyName("partId")]
        public string PartId { get; set; } = "";

        [Required]
        [JsonPropertyName("quantity")]
        public int Quantity { get; set; } = 1;

        [JsonPropertyName("label")]
        public string Label { get; set; } = ""; // Assuming Label is a string

        // Add other properties from LinkedPartInsert schema if needed
    }

    public class SkuInsert
    {
        [Required]
        [JsonPropertyName("sku")]
        public string SkuCode { get; set; } = "";

        [Required]
        [JsonPropertyName("title")]
        public string Title { get; set; } = "";

        [JsonPropertyName("description")]
        public string? Description {get; set;}

        [Required]
        [MinLength(1)]
        [JsonPropertyName("linkedParts")]
        public List<LinkedPartInsert> LinkedParts { get; set; } = new List<LinkedPartInsert>();

        // Add other properties from SkuInsert schema like storeId, folderId, etc.
        // [JsonPropertyName("storeId")] public string? StoreId {get; set;}
        // [JsonPropertyName("folderId")] public string? FolderId {get; set;}
    }
}
