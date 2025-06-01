using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text.Json;
using System.Threading.Tasks;
using PrintagoManager.Models; // Assuming models are in PrintagoManager.Models

namespace PrintagoManager.Services
{
    public class PrintagoApiClient
    {
        private readonly HttpClient _httpClient;
        private readonly string _apiKey;
        private readonly string _storeId;
        private readonly string _baseUrl = "https://api.printago.io/v1"; // From OpenAPI spec

        private static readonly JsonSerializerOptions _jsonSerializerOptions = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true, // Helpful if API casing differs slightly
            // Add other options if needed, e.g., converters for specific types
        };

        public PrintagoApiClient(string apiKey, string storeId)
        {
            if (string.IsNullOrWhiteSpace(apiKey))
                throw new ArgumentNullException(nameof(apiKey));
            if (string.IsNullOrWhiteSpace(storeId))
                throw new ArgumentNullException(nameof(storeId));

            _apiKey = apiKey;
            _storeId = storeId;

            _httpClient = new HttpClient();
            _httpClient.BaseAddress = new Uri(_baseUrl);
            _httpClient.DefaultRequestHeaders.Accept.Clear();
            _httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
            _httpClient.DefaultRequestHeaders.Add("Authorization", $"ApiKey {_apiKey}");
            _httpClient.DefaultRequestHeaders.Add("x-printago-storeid", _storeId);
            // TODO: Consider adding a User-Agent header
        }

        private async Task<T?> GetAsync<T>(string endpoint) where T : class
        {
            // Basic logging (replace with a proper logger in a real app)
            Console.WriteLine($"GET: {endpoint}");
            try
            {
                HttpResponseMessage response = await _httpClient.GetAsync(endpoint);
                if (response.IsSuccessStatusCode)
                {
                    if (response.StatusCode == System.Net.HttpStatusCode.NoContent || response.Content == null)
                    {
                        return null;
                    }
                    string content = await response.Content.ReadAsStringAsync();
                    if (string.IsNullOrWhiteSpace(content))
                    {
                        return null;
                    }
                    return JsonSerializer.Deserialize<T>(content, _jsonSerializerOptions);
                }
                else
                {
                    string errorContent = await response.Content.ReadAsStringAsync();
                    Console.WriteLine($"Error: {response.StatusCode} - {errorContent}");
                    // Consider throwing a custom exception here
                    return null;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Request Exception: {ex.Message}");
                // Consider throwing a custom exception here
                return null;
            }
        }

        private async Task<TResponse?> SendRequestAsync<TRequest, TResponse>(HttpMethod method, string endpoint, TRequest? data)
            where TRequest : class
            where TResponse : class
        {
            Console.WriteLine($"{method}: {endpoint}"); // Basic logging
            try
            {
                HttpRequestMessage request = new HttpRequestMessage(method, endpoint);
                if (data != null)
                {
                    string jsonData = JsonSerializer.Serialize(data, _jsonSerializerOptions);
                    request.Content = new StringContent(jsonData, System.Text.Encoding.UTF8, "application/json");
                    Console.WriteLine($"Request Data: {jsonData}"); // Basic logging
                }

                HttpResponseMessage response = await _httpClient.SendAsync(request);

                if (response.IsSuccessStatusCode)
                {
                    if (response.StatusCode == System.Net.HttpStatusCode.NoContent || response.Content == null)
                    {
                        return null;
                    }
                    string content = await response.Content.ReadAsStringAsync();
                     if (string.IsNullOrWhiteSpace(content))
                    {
                        return null;
                    }
                    return JsonSerializer.Deserialize<TResponse>(content, _jsonSerializerOptions);
                }
                else
                {
                    string errorContent = await response.Content.ReadAsStringAsync();
                    Console.WriteLine($"Error: {response.StatusCode} - {errorContent}");
                    // Consider throwing a custom exception here
                    return null;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Request Exception: {ex.Message}");
                return null;
            }
        }

        private async Task<TResponse?> PostAsync<TRequest, TResponse>(string endpoint, TRequest data)
            where TRequest : class where TResponse : class
        {
            return await SendRequestAsync<TRequest, TResponse>(HttpMethod.Post, endpoint, data);
        }

        private async Task<TResponse?> PatchAsync<TRequest, TResponse>(string endpoint, TRequest data)
            where TRequest : class where TResponse : class
        {
            return await SendRequestAsync<TRequest, TResponse>(new HttpMethod("PATCH"), endpoint, data);
        }

        private async Task<TResponse?> DeleteAsync<TResponse>(string endpoint, object? data = null) where TResponse : class
        {
            HttpMethod method = HttpMethod.Delete;
            Console.WriteLine($"{method}: {endpoint}");
            try
            {
                HttpRequestMessage request = new HttpRequestMessage(method, endpoint);
                if (data != null)
                {
                    string jsonData = JsonSerializer.Serialize(data, _jsonSerializerOptions);
                    request.Content = new StringContent(jsonData, System.Text.Encoding.UTF8, "application/json");
                    Console.WriteLine($"Request Data: {jsonData}");
                }

                HttpResponseMessage response = await _httpClient.SendAsync(request);
                if (response.IsSuccessStatusCode)
                {
                    if (response.StatusCode == System.Net.HttpStatusCode.NoContent || response.Content == null) return null;
                    string content = await response.Content.ReadAsStringAsync();
                    if (string.IsNullOrWhiteSpace(content)) return null;
                    return JsonSerializer.Deserialize<TResponse>(content, _jsonSerializerOptions);
                }
                else
                {
                    string errorContent = await response.Content.ReadAsStringAsync();
                    Console.WriteLine($"Error: {response.StatusCode} - {errorContent}");
                    return null;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Request Exception: {ex.Message}");
                return null;
            }
        }

        // Part Management
        public async Task<List<Part>?> GetPartsAsync()
        {
            return await GetAsync<List<Part>?>("/parts");
        }

        public async Task<Part?> GetPartAsync(string partId)
        {
            if (string.IsNullOrWhiteSpace(partId)) return null;
            return await GetAsync<Part?>($"/parts/{partId}");
        }

        public async Task<Part?> CreatePartAsync(PartInsert partData)
        {
            return await PostAsync<PartInsert, Part>("/parts", partData);
        }

        public async Task<Part?> UpdatePartAsync(string partId, PartInsert partUpdateData)
        {
            if (string.IsNullOrWhiteSpace(partId)) return null;
            return await PatchAsync<PartInsert, Part>($"/parts/{partId}", partUpdateData);
        }

        // Printer Management
        public async Task<List<Printer>?> GetPrintersAsync()
        {
            return await GetAsync<List<Printer>?>("/printers");
        }

        public async Task<Printer?> GetPrinterAsync(string printerId)
        {
            if (string.IsNullOrWhiteSpace(printerId)) return null;
            return await GetAsync<Printer?>($"/printers/{printerId}");
        }

        public async Task<Printer?> CreatePrinterAsync(PrinterInsert printerData)
        {
            return await PostAsync<PrinterInsert, Printer>("/printers", printerData);
        }

        public async Task<Printer?> UpdatePrinterAsync(string printerId, PartialPrinterUpdate printerUpdateData)
        {
            if (string.IsNullOrWhiteSpace(printerId)) return null;
            return await PatchAsync<PartialPrinterUpdate, Printer>($"/printers/{printerId}", printerUpdateData);
        }

        public async Task<List<Printer>?> SetPrinterConfigBulkAsync(SetProviderConfig configData)
        {
            // The API spec for PATCH /printers/set-config indicates it returns a list of updated printer objects.
            return await PatchAsync<SetProviderConfig, List<Printer>>("/printers/set-config", configData);
        }

        public async Task<Printer?> RenamePrinterAsync(string printerId, RenamePrinterOptions options)
        {
            if (string.IsNullOrWhiteSpace(printerId)) return null;
            // The API spec for PATCH /printers/{id}/rename indicates it returns the updated printer object.
            return await PatchAsync<RenamePrinterOptions, Printer>($"/printers/{printerId}/rename", options);
        }

        // Print Job Management
        public async Task<List<PrintJob>?> GetPrintJobsAsync()
        {
            return await GetAsync<List<PrintJob>?>("/printjobs");
        }

        public async Task<PrintJob?> GetPrintJobAsync(string printJobId) // Added specific GetPrintJob
        {
            if (string.IsNullOrWhiteSpace(printJobId)) return null;
            return await GetAsync<PrintJob?>($"/printjobs/{printJobId}");
        }

        public async Task<BuildResult?> CreateBuildAsync(BuildConfig buildConfig)
        {
            return await PostAsync<BuildConfig, BuildResult>("/printjobs/build", buildConfig);
        }

        public async Task<PrintJob?> UpdatePrintJobAsync(string jobId, PartialPrintJobInsert jobData)
        {
            if (string.IsNullOrWhiteSpace(jobId)) return null;
            return await PatchAsync<PartialPrintJobInsert, PrintJob>($"/printjobs/{jobId}", jobData);
        }

        public async Task<List<string>?> PausePrintJobsAsync(PrintJobOperationRequest request)
        {
            // Assuming the response is a list of IDs of successfully paused jobs or a success message.
            // The spec says "Array of print job IDs that were successfully paused."
            return await PostAsync<PrintJobOperationRequest, List<string>>("/printjobs/pause", request);
        }

        public async Task<List<string>?> CancelPrintJobsAsync(PrintJobOperationRequest request)
        {
            return await PostAsync<PrintJobOperationRequest, List<string>>("/printjobs/cancel", request);
        }

        public async Task<List<string>?> ResumePrintJobsAsync(PrintJobOperationRequest request)
        {
            return await PostAsync<PrintJobOperationRequest, List<string>>("/printjobs/resume", request);
        }

        // Folder Management
        public async Task<List<Folder>?> GetFoldersAsync(string type = "part") // Added GetFolders
        {
             return await GetAsync<List<Folder>?>($"/folders?type={type}");
        }

        public async Task<Folder?> CreateFolderAsync(CreateFolderRequest folderData)
        {
            return await PostAsync<CreateFolderRequest, Folder>("/folders", folderData);
        }

        // SKU Management
        public async Task<List<Sku>?> GetSkusAsync()
        {
            return await GetAsync<List<Sku>?>("/skus");
        }

        public async Task<Sku?> GetSkuAsync(string skuId) // Added specific GetSku
        {
            if (string.IsNullOrWhiteSpace(skuId)) return null;
            return await GetAsync<Sku?>($"/skus/{skuId}");
        }

        public async Task<Sku?> CreateSkuAsync(SkuInsert skuData)
        {
            return await PostAsync<SkuInsert, Sku>("/skus", skuData);
        }

        public async Task<Sku?> UpdateSkuAsync(string skuId, PartialSkuInsert skuUpdateData)
        {
            if (string.IsNullOrWhiteSpace(skuId)) return null;
            return await PatchAsync<PartialSkuInsert, Sku>($"/skus/{skuId}", skuUpdateData);
        }

        // Profile Management
        public async Task<List<Profile>?> GetProfilesAsync()
        {
            return await GetAsync<List<Profile>?>("/profiles");
        }

        public async Task<Profile?> GetProfileAsync(string profileId) // Added specific GetProfile
        {
            if (string.IsNullOrWhiteSpace(profileId)) return null;
            return await GetAsync<Profile?>($"/profiles/{profileId}");
        }

        public async Task<List<string>?> DeleteProfilesAsync(List<string> profileIds)
        {
            // The API spec for DELETE /profiles requires a body: { "ids": ["profileId1", "profileId2"] }
            // and returns { "deletedIds": ["profileId1", ...], "notFoundIds": [...] }
            // For simplicity, let's define a small helper class for the request body.
            var requestBody = new { ids = profileIds };
            // And a helper for the response. Adjust this if the actual response is more complex.
            // Assuming for now we're interested in a list of successfully deleted IDs or a generic success indicator.
            // If the response is `{"deletedIds": [], "notFoundIds": []}`, we might need a specific response model.
            // For now, let's assume a simple list of strings or a generic object indicating success.
            // The provided spec for DELETE /profiles returns 200 with an object containing deletedIds and notFoundIds.
            // So, TResponse should be a class representing that.
            // For now, I'll use a dynamic or a simple class placeholder.
            // Let's define a simple response class for this.
            // public class DeleteProfilesResponse { [JsonPropertyName("deletedIds")] public List<string>? DeletedIds { get; set; } [JsonPropertyName("notFoundIds")] public List<string>? NotFoundIds { get; set; } }
            // For now, TResponse as List<string> might be too simple if we want full info.
            // However, the prompt asked for DeleteAsync<List<string>>. This implies we expect a list of strings.
            // This might mean we only care about the "deletedIds" part or the API has an overload / different behavior.
            // Given the prompt, I will proceed with List<string> as TResponse and assume it refers to deletedIds.
            return await DeleteAsync<List<string>>("/profiles", requestBody);
        }
    }
}
