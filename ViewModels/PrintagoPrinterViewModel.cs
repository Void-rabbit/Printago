// ViewModels/PrintagoPrinterViewModel.cs
using PrintagoManager.Models;

namespace PrintagoManager.ViewModels
{
    public class PrintagoPrinterViewModel : ViewModelBase
    {
        private readonly Printer _printer;

        public string? Id => _printer.Id;
        public string? Name => _printer.Name;
        public string? Provider => _printer.Provider;
        public bool IsOnline => _printer.IsOnline;
        public string? StatusDisplay => IsOnline ? "Online" : "Offline";
        // Add more properties as needed for display, e.g., from _printer.Metadata
        public string? DeviceModel => _printer.Metadata?.ModelName; // Example from metadata

        public PrintagoPrinterViewModel(Printer printer)
        {
            _printer = printer;
        }
    }
}
