// Models/SetProviderConfig.cs
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace PrintagoManager.Models
{
    // Placeholder for BambuConfig - expand with actual fields from OpenAPI spec if available
    public class BambuConfig
    {
        [JsonPropertyName("exampleSetting")] // Replace with actual Bambu config settings
        public string? ExampleSetting { get; set; }
        // Define properties based on the "BambuConfig" schema in the OpenAPI specification
        // e.g., hostname, access_code, serial, etc.
    }

    public class SetProviderConfig
    {
        [JsonPropertyName("printerIds")]
        public List<string> PrinterIds { get; set; } = new List<string>();

        [JsonPropertyName("providerConfig")]
        public BambuConfig ProviderConfig { get; set; } = new BambuConfig();

        // Add other profile IDs if specified in the "SetProviderConfig" schema
        // e.g., [JsonPropertyName("defaultProcessProfileId")] public string? DefaultProcessProfileId { get; set; }
    }
}
