// Models/PartialPrintJobInsert.cs
using System.Text.Json.Serialization;

namespace PrintagoManager.Models
{
    public class PartialPrintJobInsert
    {
        [JsonPropertyName("status")]
        public string? Status { get; set; }

        // Add other updatable fields like label, overriddenProcessProfileId etc.
        // based on the "PartialPrintJobInsert" schema in the OpenAPI specification.
        // Example:
        // [JsonPropertyName("label")]
        // public string? Label { get; set; }

        // [JsonPropertyName("overriddenProcessProfileId")]
        // public string? OverriddenProcessProfileId { get; set; }
    }
}
