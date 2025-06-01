using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text.Json;
using System.Threading.Tasks;
using PrintagoManager.Models; // Assuming models are in PrintagoManager.Models

namespace PrintagoManager.Services
{
    public class BambuCloudClient
    {
        private readonly HttpClient _httpClient;
        private const string ApiBaseUrl = "https://api.bambulab.com/v1";
        private const string LoginEndpoint = "/user/login"; // Reasonably confirmed path

        // User-Agent and other headers based on research from bambu_api_research.md
        // (e.g., mimicking OrcaSlicer or Bambu Studio)
        private const string UserAgent = "Printago Manager/0.1"; // Or "OrcaSlicer/1.9.0" or similar
        // Add other necessary client metadata headers if identified by bambulab-authentication-cli

        private static readonly JsonSerializerOptions _jsonSerializerOptions = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true,
        };

        public BambuCloudClient()
        {
            _httpClient = new HttpClient();
            _httpClient.BaseAddress = new Uri(ApiBaseUrl);
            _httpClient.DefaultRequestHeaders.Accept.Clear();
            _httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
            _httpClient.DefaultRequestHeaders.UserAgent.ParseAdd(UserAgent);
            // TODO: Add other client metadata headers if required by the API
            // e.g., _httpClient.DefaultRequestHeaders.Add("Bambu-Client-Name", "OrcaSlicer");
        }

        public async Task<BambuAuthResponse?> AuthenticateAsync(string email, string password)
        {
            if (string.IsNullOrWhiteSpace(email) || string.IsNullOrWhiteSpace(password))
            {
                Console.WriteLine("Email and password cannot be empty."); // Basic logging
                return null;
            }

            var authRequest = new BambuAuthRequest { Email = email, Password = password };
            string jsonRequestData = JsonSerializer.Serialize(authRequest, _jsonSerializerOptions);

            Console.WriteLine($"POST: {LoginEndpoint}"); // Basic logging
            Console.WriteLine($"Request Data: {jsonRequestData}"); // Basic logging

            try
            {
                HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post, LoginEndpoint);
                request.Content = new StringContent(jsonRequestData, System.Text.Encoding.UTF8, "application/json");

                // Add specific client metadata headers if not added as default in constructor
                // request.Headers.Add("Bambu-Client-Type", "slicer");
                // request.Headers.Add("Bambu-Client-Version", "01.09.05.51");

                HttpResponseMessage response = await _httpClient.SendAsync(request);

                string responseContent = await response.Content.ReadAsStringAsync();
                Console.WriteLine($"Response Status: {response.StatusCode}"); // Basic logging
                Console.WriteLine($"Response Content: {responseContent}"); // Basic logging

                if (response.IsSuccessStatusCode)
                {
                    if (string.IsNullOrWhiteSpace(responseContent)) return null;
                    return JsonSerializer.Deserialize<BambuAuthResponse>(responseContent, _jsonSerializerOptions);
                }
                else
                {
                    Console.WriteLine($"Authentication Error: {response.StatusCode} - {responseContent}");
                    // TODO: Deserialize error response if API provides structured errors
                    return null;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Authentication Request Exception: {ex.Message}");
                return null;
            }
        }

        // Placeholder for fetching printers - still blocked by unknown endpoint
        public async Task<object?> GetPrintersAsync(string accessToken)
        {
            Console.WriteLine("GetPrintersAsync: Endpoint for listing printers is unknown and not implemented.");
            // Example of how it might look if endpoint "/user/device" was confirmed:
            // if (string.IsNullOrWhiteSpace(accessToken)) return null;
            // _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", accessToken);
            // return await GetAsync<object>("/user/device"); // Replace object with actual printer list model
            return await Task.FromResult<object?>(null);
        }

        // Placeholder for a generic GetAsync, if needed later
        // private async Task<T?> GetAsync<T>(string endpoint) where T : class { ... }
    }
}
