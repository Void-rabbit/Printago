// ViewModels/MainViewModel.cs
using System.Collections.ObjectModel;
using System.Threading.Tasks;
using PrintagoManager.Services;
using PrintagoManager.Models;
using System.Linq; // Required for Select

namespace PrintagoManager.ViewModels
{
    public class MainViewModel : ViewModelBase
    {
        private PrintagoApiClient _printagoClient;
        // TODO: Securely load APIKey and StoreID from config/settings
        private const string PRINTAGO_API_KEY = "uw9cgpqf3cav0jt68iuhroqmpnpzylgyd9v1hnh4qj1dgxc9u8avxvrg0dub4jj10q1z9uy6";
        private const string PRINTAGO_STORE_ID = "jma9q6h3iahb9czvy0ton79n";

        public ObservableCollection<PrintagoPrinterViewModel> PrintagoPrinters { get; }

        private string _printagoStatus = "";
        public string PrintagoStatus
        {
            get => _printagoStatus;
            set { _printagoStatus = value; OnPropertyChanged(); }
        }

        public ICommand LoadPrintagoPrintersCommand { get; } // Added for refresh button

        public MainViewModel()
        {
            _printagoClient = new PrintagoApiClient(PRINTAGO_API_KEY, PRINTAGO_STORE_ID);
            PrintagoPrinters = new ObservableCollection<PrintagoPrinterViewModel>();
            LoadPrintagoPrintersCommand = new RelayCommand(async _ => await LoadPrintagoPrintersAsync()); // Initialize command
        }

        public async Task LoadPrintagoPrintersAsync()
        {
            PrintagoStatus = "Loading Printago printers...";
            PrintagoPrinters.Clear();
            try
            {
                var printers = await _printagoClient.GetPrintersAsync();
                if (printers != null && printers.Any())
                {
                    foreach (var printer in printers)
                    {
                        PrintagoPrinters.Add(new PrintagoPrinterViewModel(printer));
                    }
                    PrintagoStatus = $"Loaded {PrintagoPrinters.Count} printers from Printago.";
                }
                else
                {
                    PrintagoStatus = "No printers found for your Printago store, or failed to load.";
                }
            }
            catch (System.Exception ex)
            {
                PrintagoStatus = $"Error loading Printago printers: {ex.Message}";
                System.Console.WriteLine($"Printago Load Error: {ex}"); // For debug
            }
        }
    }
}
