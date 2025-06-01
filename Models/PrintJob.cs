// Models/PrintJob.cs
using System;
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace PrintagoManager.Models
{
    public class PrintJob
    {
        [JsonPropertyName("id")]
        public string? Id { get; set; }

        [JsonPropertyName("partBuildId")]
        public string? PartBuildId { get; set; }

        [JsonPropertyName("partName")]
        public string? PartName { get; set; }

        [JsonPropertyName("status")]
        public string? Status { get; set; } // "pending", "printing", etc.

        [JsonPropertyName("queueOrder")]
        public int QueueOrder { get; set; }

        [JsonPropertyName("assignedPrinterId")]
        public string? AssignedPrinterId { get; set; }

        // Required Printer Tags (complex object, placeholder for now or map if simple)
        // [JsonPropertyName("requiredPrinterTags")]
        // public object? RequiredPrinterTags { get; set; }

        [JsonPropertyName("createdAt")]
        public DateTime CreatedAt { get; set; }

        [JsonPropertyName("updatedAt")]
        public DateTime UpdatedAt { get; set; }
        // Add other relevant properties
    }
}
