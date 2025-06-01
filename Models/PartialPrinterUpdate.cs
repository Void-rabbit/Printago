// Models/PartialPrinterUpdate.cs
using System.Text.Json.Serialization;

namespace PrintagoManager.Models
{
    public class PartialPrinterUpdate
    {
        [JsonPropertyName("name")]
        public string? Name { get; set; }

        [JsonPropertyName("enabled")]
        public bool? Enabled { get; set; }

        // Add other updatable fields from PartialPrinterUpdate schema
        [JsonPropertyName("metadata")]
        public PrinterMetadata? Metadata { get; set; } // Using existing PrinterMetadata
    }
}
