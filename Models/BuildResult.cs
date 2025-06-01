// Models/BuildResult.cs
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace PrintagoManager.Models
{
    // Simplified - expand based on spec for PartBuild
    public class PartBuild
    {
        [JsonPropertyName("partBuildId")]
        public string? PartBuildId { get; set; }

        [JsonPropertyName("partId")]
        public string? PartId { get; set; }

        [JsonPropertyName("quantity")]
        public int Quantity { get; set; }

        [JsonPropertyName("printJobIds")]
        public List<string>? PrintJobIds {get; set;}

        // Add other properties from PartBuild schema like Label, Status, etc.
    }

    // Simplified - expand based on spec for SkuBuild
    public class SkuBuild
    {
        [JsonPropertyName("skuBuildId")]
        public string? SkuBuildId { get; set; }

        [JsonPropertyName("skuId")]
        public string? SkuId { get; set; }

        [JsonPropertyName("quantity")]
        public int Quantity { get; set; }

        [JsonPropertyName("partBuilds")] // SkuBuild contains PartBuilds
        public List<PartBuild>? PartBuilds { get; set; }

        // Add other properties from SkuBuild schema
    }

    public class BuildResult
    {
        [JsonPropertyName("partBuilds")]
        public List<PartBuild>? PartBuilds { get; set; }

        [JsonPropertyName("skuBuilds")]
        public List<SkuBuild>? SkuBuilds { get; set; }

        // Could also include overall build ID if the API provides one at this level
        // [JsonPropertyName("buildId")]
        // public string? BuildId { get; set; }
    }
}
