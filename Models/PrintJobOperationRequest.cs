// Models/PrintJobOperationRequest.cs
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace PrintagoManager.Models
{
    public class PrintJobOperationRequest
    {
        [JsonPropertyName("printJobIds")]
        public List<string> PrintJobIds { get; set; } = new List<string>();
    }
}
