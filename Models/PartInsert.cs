// Models/PartInsert.cs
using System.Collections.Generic;
using System.Text.Json.Serialization;
using System.ComponentModel.DataAnnotations; // For potential validation attributes

namespace PrintagoManager.Models
{
    public class PartInsert
    {
        [Required]
        [StringLength(64, MinimumLength = 1)]
        [JsonPropertyName("name")]
        public string Name { get; set; } = "";

        [Required]
        [JsonPropertyName("type")]
        public string Type { get; set; } = ""; // "scad", "stl", "step", "3mf", "gcode3mf"

        [JsonPropertyName("description")]
        public string? Description { get; set; } = "";

        [Required]
        [MinLength(1)]
        [JsonPropertyName("fileUris")]
        public List<string> FileUris { get; set; } = new List<string>();

        // fileHashes is required by Part but not by PartInsert in the provided spec for POST.
        // If API requires it for POST, it should be added here.
        // For PATCH, it's optional.

        // Other properties from PartInsert schema...
        // [JsonPropertyName("parameters")]
        // public List<PartParameter>? Parameters { get; set; }

        // [JsonPropertyName("printTags")]
        // public Tags? PrintTags { get; set; }

        // [JsonPropertyName("allowedFilamentTypes")]
        // public List<string>? AllowedFilamentTypes { get; set; }
    }
}
