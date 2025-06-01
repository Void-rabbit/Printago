// Services/TokenStorageService.cs
using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using PrintagoManager.Models; // For BambuAuthResponse

namespace PrintagoManager.Services
{
    public class TokenStorageService
    {
        private static readonly string AppName = "PrintagoManager";
        // Store token in user's local app data folder
        private static readonly string TokenFilePath = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            AppName,
            "auth.token");
        private static readonly byte[] Entropy = Encoding.UTF8.GetBytes("PrintagoManagerSalt"); // Optional salt

        public void SaveToken(BambuAuthResponse tokenData)
        {
            try
            {
                string jsonToken = JsonSerializer.Serialize(tokenData);
                byte[] plainTextBytes = Encoding.UTF8.GetBytes(jsonToken);

                // Encrypt the data using ProtectedData (User scope)
                byte[] encryptedBytes = ProtectedData.Protect(plainTextBytes, Entropy, DataProtectionScope.CurrentUser);

                Directory.CreateDirectory(Path.GetDirectoryName(TokenFilePath)!); // Ensure directory exists
                File.WriteAllBytes(TokenFilePath, encryptedBytes);
                Console.WriteLine($"Token saved to: {TokenFilePath}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error saving token: {ex.Message}");
                // Handle exception (e.g., log it)
            }
        }

        public BambuAuthResponse? LoadToken()
        {
            try
            {
                if (!File.Exists(TokenFilePath))
                {
                    return null;
                }

                byte[] encryptedBytes = File.ReadAllBytes(TokenFilePath);

                // Decrypt the data
                byte[] plainTextBytes = ProtectedData.Unprotect(encryptedBytes, Entropy, DataProtectionScope.CurrentUser);

                string jsonToken = Encoding.UTF8.GetString(plainTextBytes);
                Console.WriteLine("Token loaded successfully.");
                // TODO: Implement token expiry check here based on ExpiresIn and stored time.
                return JsonSerializer.Deserialize<BambuAuthResponse>(jsonToken);
            }
            catch (FileNotFoundException)
            {
                Console.WriteLine("Token file not found.");
                return null;
            }
            catch (CryptographicException ex)
            {
                Console.WriteLine($"Error decrypting token (maybe corrupted or from different user/machine): {ex.Message}");
                ClearToken(); // Delete corrupted token
                return null;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error loading token: {ex.Message}");
                return null;
            }
        }

        public void ClearToken()
        {
            try
            {
                if (File.Exists(TokenFilePath))
                {
                    File.Delete(TokenFilePath);
                    Console.WriteLine("Token cleared.");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error clearing token: {ex.Message}");
            }
        }
    }
}
