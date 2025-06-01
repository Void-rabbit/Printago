using System.Text.Json.Serialization;

namespace PrintagoManager.Models
{
    public class PrinterMetadata // Assuming BambuPrinterMetadata from spec
    {
        [JsonPropertyName("name")]
        public string? Name {get; set;} // This might be the same as the top-level name

        [JsonPropertyName("dev_id")]
        public string? DeviceId {get; set;} // Different from top-level Id

        [JsonPropertyName("online")]
        public bool Online { get; set; }

        [JsonPropertyName("print_status")]
        public string? PrintStatus { get; set; }

        [JsonPropertyName("dev_model_name")]
        public string? ModelName {get; set;}

        // Other metadata fields
    }
    public class Printer
    {
        [JsonPropertyName("id")]
        public string? Id { get; set; }

        [JsonPropertyName("name")]
        public string? Name { get; set; }

        [JsonPropertyName("provider")]
        public string? Provider { get; set; } // "Bambu", "Prusa", etc.

        [JsonPropertyName("isOnline")] // This field is in the OpenAPI spec for Printer
        public bool IsOnline { get; set; }

        [JsonPropertyName("storeId")]
        public string? StoreId { get; set; }

        [JsonPropertyName("createdAt")]
        public DateTime CreatedAt { get; set; }

        [JsonPropertyName("updatedAt")]
        public DateTime UpdatedAt { get; set; }

        [JsonPropertyName("metadata")]
        public PrinterMetadata? Metadata { get; set; }
        // Add other relevant properties from OpenAPI spec for Printer schema later
    }
}
