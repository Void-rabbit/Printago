// Models/BuildConfig.cs
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace PrintagoManager.Models
{
    // Simplified for now - expand based on spec for PartBuildConfig and SkuBuildConfig
    public class PartBuildConfig
    {
        [JsonPropertyName("partId")]
        public string PartId { get; set; } = "";

        [JsonPropertyName("quantity")]
        public int Quantity { get; set; } = 1;

        // Add other properties from PartBuildConfig schema if needed
        // e.g., [JsonPropertyName("label")] public string? Label { get; set; }
        // e.g., [JsonPropertyName("overriddenProcessProfileId")] public string? OverriddenProcessProfileId { get; set; }
    }

    public class SkuBuildConfig
    {
        [JsonPropertyName("skuId")]
        public string SkuId { get; set; } = "";

        [JsonPropertyName("quantity")]
        public int Quantity { get; set; } = 1;

        // Add other properties from SkuBuildConfig schema if needed
    }

    public class BuildConfig
    {
        [JsonPropertyName("parts")]
        public List<PartBuildConfig>? Parts { get; set; }

        [JsonPropertyName("skus")]
        public List<SkuBuildConfig>? Skus { get; set; }

        // Add other properties from BuildConfig schema if needed
        // e.g., [JsonPropertyName("targetPrinterId")] public string? TargetPrinterId { get; set; }
        // e.g., [JsonPropertyName("label")] public string? Label { get; set; }
    }
}
