// Models/RenamePrinterOptions.cs
using System.Text.Json.Serialization;

namespace PrintagoManager.Models
{
    public class RenamePrinterOptions
    {
        [JsonPropertyName("name")]
        public string Name { get; set; } = "";
    }
}
