// MainWindow.xaml.cs
using System.Windows;
using PrintagoManager.ViewModels;
using PrintagoManager.Services; // Required for TokenStorageService
using System; // Required for Console.WriteLine

namespace PrintagoManager
{
    public partial class MainWindow : Window
    {
        private LoginViewModel _loginViewModel;
        private MainViewModel _mainViewModel; // Added
        private readonly TokenStorageService _tokenStorageService;

        public MainWindow()
        {
            InitializeComponent();
            _tokenStorageService = new TokenStorageService();

            _loginViewModel = new LoginViewModel(_tokenStorageService);
            // Set DataContext for the LoginPanel specifically
            LoginPanel.DataContext = _loginViewModel;

            _mainViewModel = new MainViewModel(); // Instantiate MainViewModel
            MainContentPanel.DataContext = _mainViewModel; // Set for the main content area

            _loginViewModel.LoginSuccessful += OnLoginSuccessful;
            _loginViewModel.LoggedOut += OnLoggedOut;

            AttemptAutoLogin();
        }

        private void AttemptAutoLogin() // Changed from async void
        {
            var storedToken = _tokenStorageService.LoadToken();
            if (storedToken != null && !string.IsNullOrEmpty(storedToken.AccessToken))
            {
                Console.WriteLine($"Found stored token for user: {storedToken.Email ?? storedToken.UserName}");
                _loginViewModel.LoginStatus = $"Welcome back {storedToken.UserName ?? storedToken.Email}!";
                OnLoginSuccessful();
            }
            else
            {
                ShowLoginView();
            }
        }

        private async void OnLoginSuccessful() // Made async
        {
            LoginPanel.Visibility = Visibility.Collapsed;
            MainContentPanel.Visibility = Visibility.Visible;
            await _mainViewModel.LoadPrintagoPrintersAsync(); // Load data for the main view
        }

        private void OnLoggedOut()
        {
            ShowLoginView();
        }

        private void ShowLoginView()
        {
            LoginPanel.Visibility = Visibility.Visible;
            MainContentPanel.Visibility = Visibility.Collapsed;

            if (LoginPanel.DataContext is LoginViewModel lvm)
            {
                // lvm.Email = ""; // Optional: Clear email on logout
                UserPasswordBox.Clear(); // Clear password box content
                lvm.LoginStatus = ""; // Clear status messages
            }
        }
    }
}
