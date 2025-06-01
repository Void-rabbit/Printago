// Models/CreateFolderRequest.cs
using System.Text.Json.Serialization;
using System.ComponentModel.DataAnnotations;

namespace PrintagoManager.Models
{
    public class CreateFolderRequest
    {
        [Required]
        [JsonPropertyName("name")]
        public string Name { get; set; } = "";

        [Required]
        [JsonPropertyName("type")]
        public string Type { get; set; } = ""; // "part" or "sku"

        [JsonPropertyName("parentId")]
        public string? ParentId { get; set; }
    }
}
