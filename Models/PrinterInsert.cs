// Models/PrinterInsert.cs
using System.Text.Json.Serialization;

namespace PrintagoManager.Models
{
    // Assuming BambuPrinterMetadata is defined elsewhere, e.g. in Models/Printer.cs
    // If not, it needs to be defined here or in a common place.
    // For this example, let's assume it exists or is simple enough to be inlined if needed.
    // public class BambuPrinterMetadata { /* ... properties ... */ }

    public class PrinterInsert
    {
        [JsonPropertyName("name")]
        public string Name { get; set; } = "";

        [JsonPropertyName("provider")]
        public string Provider { get; set; } = "Bambu"; // Default or make required

        [JsonPropertyName("deviceId")]
        public string? DeviceId { get; set; } // For Bambu, this is serial

        [JsonPropertyName("nozzleDiameter")]
        public string NozzleDiameter { get; set; } = "0.4"; // Default or make required

        [JsonPropertyName("enabled")]
        public bool Enabled { get; set; } = true;

        // Add other fields from PrinterInsert schema like metadata, integrationId, commMethod etc.
        [JsonPropertyName("metadata")]
        public BambuPrinterMetadata? Metadata { get; set; } // Re-use if defined (needs BambuPrinterMetadata definition)
    }
}
