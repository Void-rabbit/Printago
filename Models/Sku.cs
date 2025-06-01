// Models/Sku.cs
using System;
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace PrintagoManager.Models
{
    // Forward declare LinkedPart if it's complex and defined elsewhere, or define simply here
    public class SkuLinkedPart // Simplified for this example
    {
        [JsonPropertyName("partId")]
        public string? PartId { get; set; }
        [JsonPropertyName("quantity")]
        public int Quantity { get; set; }
    }

    public class Sku
    {
        [JsonPropertyName("id")]
        public string? Id { get; set; }

        [JsonPropertyName("sku")] // This is the SKU identifier string
        public string? SkuCode { get; set; }

        [JsonPropertyName("title")]
        public string? Title { get; set; }

        [JsonPropertyName("description")]
        public string? Description { get; set; }

        [JsonPropertyName("linkedParts")]
        public List<SkuLinkedPart>? LinkedParts { get; set; }
        // Add other relevant properties
    }
}
