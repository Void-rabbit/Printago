// ViewModels/LoginViewModel.cs
using System.Threading.Tasks;
using System.Windows.Input;
using PrintagoManager.Services; // For BambuCloudClient
using PrintagoManager.Models;   // For BambuAuthResponse

namespace PrintagoManager.ViewModels
{
    public class LoginViewModel : ViewModelBase
    {
        private string _email = "";
        public string Email
        {
            get => _email;
            set { _email = value; OnPropertyChanged(); }
        }

        // Password will be handled via PasswordBox in View code-behind for better security practice

        private string _loginStatus = "";
        public string LoginStatus
        {
            get => _loginStatus;
            set { _loginStatus = value; OnPropertyChanged(); }
        }

        private bool _isLoggingIn;
        public bool IsLoggingIn { get => _isLoggingIn; set { _isLoggingIn = value; OnPropertyChanged(); }}

        public ICommand LoginCommand { get; }
        private BambuCloudClient _bambuClient;

        public event System.Action? LoginSuccessful; // Event to notify view
                public event System.Action? LoggedOut; // Event to notify view of logout

                private readonly TokenStorageService _tokenStorageService;
                public ICommand LogoutCommand { get; }


                public LoginViewModel(TokenStorageService tokenStorageService) // Modified constructor
        {
            _bambuClient = new BambuCloudClient();
                    _tokenStorageService = tokenStorageService; // Injected
            LoginCommand = new RelayCommand(async (passwordBox) => await ExecuteLoginAsync(passwordBox as System.Windows.Controls.PasswordBox),
                                            (passwordBox) => !IsLoggingIn && passwordBox is System.Windows.Controls.PasswordBox);
                    LogoutCommand = new RelayCommand(ExecuteLogout); // Initialize LogoutCommand
                }

                private void ExecuteLogout(object? parameter)
                {
                    _tokenStorageService.ClearToken();
                    LoginStatus = "Logged out.";
                    // Clear sensitive fields if any are stored in ViewModel (Email is fine to keep for convenience)
                    // PasswordBox should be cleared by the View if needed
                    LoggedOut?.Invoke();
                    Console.WriteLine("Executed Logout Command");
        }

        private async Task ExecuteLoginAsync(System.Windows.Controls.PasswordBox? passwordBox)
        {
            if (passwordBox == null) return;
            string? password = passwordBox.Password;
            if (string.IsNullOrWhiteSpace(Email) || string.IsNullOrWhiteSpace(password))
            {
                LoginStatus = "Email and password cannot be empty.";
                return;
            }

            IsLoggingIn = true;
            LoginStatus = "Logging in...";
            try
            {
                BambuAuthResponse? authResponse = await _bambuClient.AuthenticateAsync(Email, password);
                if (authResponse != null && !string.IsNullOrEmpty(authResponse.AccessToken))
                {
                    LoginStatus = $"Login Successful! Welcome {authResponse.UserName ?? authResponse.Email}";
                            _tokenStorageService.SaveToken(authResponse); // Save token
                            // TODO: Handle token expiry (authResponse.ExpiresIn) - possibly in TokenStorageService.LoadToken
                    System.Console.WriteLine($"Access Token: {authResponse.AccessToken}"); // For debug
                    LoginSuccessful?.Invoke();
                }
                else
                {
                    LoginStatus = "Login Failed. Check credentials or API response.";
                }
            }
            catch (System.Exception ex)
            {
                LoginStatus = $"Login Error: {ex.Message}";
            }
            finally { IsLoggingIn = false; }
        }
    }
}
