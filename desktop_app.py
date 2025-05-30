import sys
import os # Added for resource_path
from PySide6.QtWidgets import ( # Changed from PySide2
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QWidget, QMessageBox, QDialog, QDialogButtonBox, QFormLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QStatusBar, QToolBar, QAction,
    QStackedWidget, QProgressBar, QTabWidget, QComboBox, QHBoxLayout
)
from PySide6.QtCore import Qt, Slot # Changed from PySide2
from PySide6.QtGui import QColor # Changed from PySide2
import bambu_cloud_client as cloud_client

# Helper function for PyInstaller one-file bundle
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Views
class PrinterDetailsView(QWidget):
    def __init__(self, printer_id, printer_name, parent=None):
        super().__init__(parent)
        self.printer_id = printer_id
        self.printer_name = printer_name
        self.setObjectName("PrinterDetailsView")

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        title_label = QLabel(f"Details for {self.printer_name} (ID: {self.printer_id})")
        title_label.setAlignment(Qt.AlignCenter)
        # Basic inline styling for prominence, QSS can override
        title_label.setStyleSheet("QLabel { font-size: 16pt; font-weight: bold; margin-bottom: 10px; }")
        main_layout.addWidget(title_label)

        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # Tab 1: Status & Controls
        status_controls_tab = QWidget()
        status_layout = QFormLayout(status_controls_tab)

        status_layout.addRow(QLabel("Nozzle Temperature:"), QLabel("220°C / 220°C (Mocked)"))
        status_layout.addRow(QLabel("Bed Temperature:"), QLabel("60°C / 60°C (Mocked)"))
        status_layout.addRow(QLabel("Current Print Job:"), QLabel("example_part_v2.gcode (Mocked)"))

        progress_bar = QProgressBar()
        progress_bar.setValue(67) # Mocked value
        status_layout.addRow(QLabel("Progress:"), progress_bar)

        status_layout.addRow(QLabel("Time Remaining:"), QLabel("Approx. 35 mins (Mocked)"))

        controls_box = QHBoxLayout() # For buttons in a row
        controls_box.addWidget(QPushButton("Pause Print"))
        controls_box.addWidget(QPushButton("Resume Print"))
        controls_box.addWidget(QPushButton("Cancel Print"))
        status_layout.addRow(controls_box) # Add button layout as a single row in form layout

        tab_widget.addTab(status_controls_tab, "Status & Controls")

        # Tab 2: Print Profiles
        profiles_tab = QWidget()
        profiles_layout_main = QVBoxLayout(profiles_tab) # Main layout for this tab

        profiles_form_layout = QFormLayout() # Form layout for labeled controls
        profile_combo = QComboBox()
        profile_combo.addItems(["0.2mm Standard PLA", "0.16mm High Quality PETG", "0.28mm Draft ABS"])
        profiles_form_layout.addRow(QLabel("Available Print Profiles:"), profile_combo)
        profiles_layout_main.addLayout(profiles_form_layout) # Add form to main layout

        profiles_layout_main.addWidget(QPushButton("View/Edit Selected Profile"))
        profiles_layout_main.addStretch() # Push elements to top
        tab_widget.addTab(profiles_tab, "Print Profiles")

        # Tab 3: Device Information
        device_info_tab = QWidget()
        device_info_layout = QFormLayout(device_info_tab)
        device_info_layout.addRow(QLabel("Model:"), QLabel("Bambu Lab X1 Carbon (Mocked)"))
        device_info_layout.addRow(QLabel("Serial Number:"), QLabel(self.printer_id + " (Mocked S/N)"))
        device_info_layout.addRow(QLabel("Firmware Version:"), QLabel("01.06.05.01 (Mocked)"))
        device_info_layout.addRow(QLabel("IP Address:"), QLabel("192.168.1.101 (Mocked)"))
        tab_widget.addTab(device_info_tab, "Device Information")

        start_job_button = QPushButton("Start New Print Job with this Printer")
        main_layout.addWidget(start_job_button)
        main_layout.addStretch() # Pushes the button to bottom if main_layout has space

class SettingsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SettingsView")
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        title_label = QLabel("Application Settings")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("QLabel { font-size: 16pt; font-weight: bold; margin-bottom: 10px; }")
        main_layout.addWidget(title_label)

        form_layout = QFormLayout()

        # Theme Selection
        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark (Default)", "Light (Not Implemented)"])
        form_layout.addRow(theme_label, self.theme_combo)

        main_layout.addLayout(form_layout)
        main_layout.addSpacing(20)

        # Printago Store Configuration
        printago_title_label = QLabel("Printago Store Integration (Placeholder)")
        printago_title_label.setStyleSheet("QLabel { font-size: 12pt; font-weight: bold; margin-top:10px; }")
        main_layout.addWidget(printago_title_label)

        printago_form_layout = QFormLayout()
        self.printago_api_key_input = QLineEdit()
        self.printago_api_key_input.setPlaceholderText("Enter Printago API Key (if applicable)")
        printago_form_layout.addRow(QLabel("Printago API Key:"), self.printago_api_key_input)

        self.printago_store_id_input = QLineEdit()
        self.printago_store_id_input.setPlaceholderText("Enter Printago Store ID (if applicable)")
        printago_form_layout.addRow(QLabel("Printago Store ID:"), self.printago_store_id_input)

        main_layout.addLayout(printago_form_layout)
        main_layout.addWidget(QPushButton("Save Printago Settings"))
        main_layout.addSpacing(20)

        main_layout.addWidget(QPushButton("Check for Updates"))
        main_layout.addStretch() # Push all content to the top


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login - Bambu Lab Cloud")
        self.setModal(True) # Block interaction with the main window
        self.layout = QVBoxLayout(self)

        self.status_label = QLabel("Please login to your Bambu Lab account.")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        form_layout = QFormLayout()
        self.email_input = QLineEdit() # Renamed from username_input
        self.email_input.setPlaceholderText("Enter your Bambu Lab email")
        form_layout.addRow("Email:", self.email_input) # Changed label

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Password:", self.password_input)
        self.layout.addLayout(form_layout)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

        self.auth_data = None # To store authentication result

    def accept(self):
        email = self.email_input.text() # Changed from username_input
        password = self.password_input.text()

        if not email or not password: # Changed from username
            QMessageBox.warning(self, "Login Error", "Email and password cannot be empty.") # Changed message
            return # Keep dialog open

        self.status_label.setText("Authenticating...")
        QApplication.processEvents()

        self.auth_data = cloud_client.authenticate(email, password) # Pass email

        if self.auth_data and self.auth_data.get("access_token"):
            cloud_client.save_token(self.auth_data)
            QMessageBox.information(self, "Login Success", "Login successful!")
            super().accept() # Close dialog with QDialog.Accepted state
        else:
            self.status_label.setText("Login failed. Check credentials or console.")
            QMessageBox.critical(self, "Login Failed", "Login failed. Please check your credentials or console output for more details.")
            # Keep dialog open for another attempt

    def get_auth_data(self):
        return self.auth_data


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Printago Manager - Bambu Lab Cloud")
        self.setGeometry(100, 100, 800, 600)
        self.current_token_data = None

        self.create_actions()
        self.create_toolbar()
        self.create_status_bar()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.printers_view_widget = QWidget()
        printers_layout = QVBoxLayout(self.printers_view_widget)

        printers_list_label = QLabel("Discovered Cloud Printers:")
        printers_layout.addWidget(printers_list_label)

        self.printers_table = QTableWidget()
        self.printers_table.setColumnCount(3)
        self.printers_table.setHorizontalHeaderLabels(["Name", "Status", "Actions"])
        self.printers_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.printers_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)
        self.printers_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)
        self.printers_table.setEditTriggers(QTableWidget.NoEditTriggers) # Read-only
        printers_layout.addWidget(self.printers_table)

        self.refresh_printers_button = QPushButton("Refresh Printers List")
        self.refresh_printers_button.clicked.connect(self.handle_refresh_printers_list)
        printers_layout.addWidget(self.refresh_printers_button)

        self.stacked_widget.addWidget(self.printers_view_widget) # Index 0 - Printers View

        self.settings_view = SettingsView(self) # Index 1 - Settings View
        self.stacked_widget.addWidget(self.settings_view)

        # Placeholder for where PrinterDetailsView instances will be managed
        # We won't add a generic one to the stack initially,
        # but rather create/show it when "View Details" is clicked.
        # For simplicity in this step, we'll just ensure navigation can switch to index 0 or 1.

        self.check_initial_login()

    def create_actions(self):
        self.printers_action = QAction("Printers", self)
        self.printers_action.triggered.connect(self.show_printers_view)
        self.settings_action = QAction("Settings", self)
        self.settings_action.triggered.connect(self.show_settings_view)
        self.logout_action = QAction("Logout", self)
        self.logout_action.triggered.connect(self.handle_logout)
        # Login action might be added if user logs out and wants to log back in
        self.login_action = QAction("Login", self)
        self.login_action.triggered.connect(self.show_login_dialog_manual)


    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.addAction(self.printers_action)
        toolbar.addAction(self.settings_action)
        toolbar.addSeparator()
        toolbar.addAction(self.logout_action)
        toolbar.addAction(self.login_action) # Initially login might be hidden if auto-logged in

    def create_status_bar(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready.")

    def show_printers_view(self):
        self.stacked_widget.setCurrentWidget(self.printers_view_widget)
        self.statusBar.showMessage("Viewing Printers.")
        # If token is valid, refresh printer list when switching to this view
        if self.current_token_data and self.current_token_data.get("access_token"):
            self.fetch_and_display_printers(self.current_token_data.get("access_token"))
        else:
            self.printers_table.setRowCount(0) # Clear table if not logged in
            self.statusBar.showMessage("Not logged in. Please login to view printers.")


    def show_settings_view(self):
        self.stacked_widget.setCurrentWidget(self.settings_view)
        self.statusBar.showMessage("Viewing Settings.")

    def check_initial_login(self):
        self.statusBar.showMessage("Checking for saved authentication...")
        self.current_token_data = cloud_client.load_token()
        if self.current_token_data and self.current_token_data.get("access_token"):
            # TODO: Add proper token expiry check here.
            self.statusBar.showMessage("Token found. Fetching printers...")
            self.fetch_and_display_printers(self.current_token_data["access_token"])
            self.show_printers_view() # Show printers view by default
            self.login_action.setEnabled(False) # Disable login if already logged in
        else:
            self.statusBar.showMessage("No valid token. Please login.")
            self.show_login_dialog_initial()
            self.login_action.setEnabled(True)


    def show_login_dialog_initial(self):
        """Show login dialog on startup if no token."""
        login_dialog = LoginDialog(self)
        if login_dialog.exec_() == QDialog.Accepted:
            self.current_token_data = login_dialog.get_auth_data()
            if self.current_token_data and self.current_token_data.get("access_token"):
                self.statusBar.showMessage("Login successful. Fetching printers...")
                self.fetch_and_display_printers(self.current_token_data["access_token"])
                self.show_printers_view()
                self.login_action.setEnabled(False)
            else: # Should not happen if dialog logic is correct
                self.statusBar.showMessage("Login process completed but no valid token. Please try again.")
                self.show_printers_view() # Show empty printer view
                self.printers_table.setRowCount(0)
                self.login_action.setEnabled(True)

        else: # User cancelled login
            self.statusBar.showMessage("Login cancelled by user. Application may have limited functionality.")
            self.show_printers_view() # Show empty printer view
            self.printers_table.setRowCount(0)
            self.login_action.setEnabled(True)

    def show_login_dialog_manual(self):
        """Show login dialog when user clicks Login action."""
        if self.current_token_data and self.current_token_data.get("access_token"):
            QMessageBox.information(self, "Already Logged In", "You are already logged in.")
            return

        login_dialog = LoginDialog(self)
        if login_dialog.exec_() == QDialog.Accepted:
            self.current_token_data = login_dialog.get_auth_data()
            if self.current_token_data and self.current_token_data.get("access_token"):
                self.statusBar.showMessage("Login successful. Fetching printers...")
                self.fetch_and_display_printers(self.current_token_data["access_token"])
                self.show_printers_view()
                self.login_action.setEnabled(False)
            else:
                self.statusBar.showMessage("Login process completed but no valid token. Please try again.")
                self.show_printers_view()
                self.printers_table.setRowCount(0)
                self.login_action.setEnabled(True)

        else:
            self.statusBar.showMessage("Login cancelled.")
            self.login_action.setEnabled(True)


    def fetch_and_display_printers(self, access_token):
        self.printers_table.setRowCount(0) # Clear existing items
        self.statusBar.showMessage("Fetching printers...")
        QApplication.processEvents()

        printers = cloud_client.get_printers(access_token)
        if printers is not None:
            if printers:
                self.printers_table.setRowCount(len(printers))
                for row, printer_data in enumerate(printers):
                    name = printer_data.get('name', 'Unknown Printer')
                    dev_id = printer_data.get('dev_id', 'N/A') # Store for later

                    # Mock status based on some printer data if available, else default
                    # This is very basic, actual status would come from a different field or logic
                    status_text = printer_data.get('print_status', "Idle") # Example: 'printing', 'finish', 'idle'
                    status_item = QTableWidgetItem(status_text)
                    if status_text.lower() == "idle" or status_text.lower() == "finish":
                        status_item.setForeground(QColor("green"))
                    elif status_text.lower() == "printing":
                        status_item.setForeground(QColor("yellow"))
                    else: # error, offline etc.
                        status_item.setForeground(QColor("red"))

                    self.printers_table.setItem(row, 0, QTableWidgetItem(name))
                    self.printers_table.setItem(row, 1, status_item)

                    # Store dev_id with the name item for later use
                    self.printers_table.item(row, 0).setData(Qt.UserRole, dev_id)

                    # Placeholder for "View Details" button
                    btn_details = QPushButton("View Details")
                    btn_details.clicked.connect(lambda checked, pid=dev_id, pname=name: self.show_printer_details_view(pid, pname))
                    self.printers_table.setCellWidget(row, 2, btn_details)

                self.statusBar.showMessage(f"Found {len(printers)} printers.")
            else:
                self.statusBar.showMessage("No printers found for this account.")
        else:
            self.statusBar.showMessage("Failed to fetch printers. Token might be expired or invalid.")
            QMessageBox.warning(self, "Fetch Printers Failed", "Could not fetch printers. The access token might be expired or invalid.")
            self.current_token_data = None # Invalidate token
            cloud_client.save_token(None) # Clear stored token
            self.login_action.setEnabled(True)


    def handle_refresh_printers_list(self):
        if self.current_token_data and self.current_token_data.get("access_token"):
            self.fetch_and_display_printers(self.current_token_data["access_token"])
        else:
            self.statusBar.showMessage("No valid token. Please login first.")
            QMessageBox.information(self, "Refresh Printers", "No valid token found. Please login first.")
            self.show_login_dialog_manual()


    def handle_logout(self):
        token_path = cloud_client.get_token_storage_path()
        if token_path.exists():
            try:
                token_path.unlink() # Remove the token file
            except Exception as e:
                QMessageBox.warning(self, "Logout Error", f"Could not clear token file: {e}")

        self.current_token_data = None
        self.printers_table.setRowCount(0)
        self.statusBar.showMessage("Logged out. Token cleared.")
        QMessageBox.information(self, "Logout", "Successfully logged out and cleared saved token.")
        self.login_action.setEnabled(True)
        # Optionally, switch to a logged-out view or show login dialog again
        self.show_login_dialog_manual() # Prompt to log in again after logout

    @Slot(str, str)
    def show_printer_details_view(self, printer_id, printer_name):
        # Check if a details view for this printer_id already exists
        # For simplicity, we create a new one each time or have a placeholder.
        # A more robust approach would manage a dictionary of printer detail views.

        # If you want to add it to the stacked widget and switch:
        # 1. Remove previous printer detail view if any
        # 2. Create new PrinterDetailsView
        # 3. Add to stacked widget
        # 4. Switch to it

        # For now, let's just show a message or a dedicated (but simple) details view
        # that is not part of the main stack to keep this step focused.
        # Or, we can add one instance and update its content.

        # Find if a PrinterDetailsView already exists in the stack (e.g. at index 2)
        # This is a simplified approach; usually, you'd manage views more dynamically.

        details_widget_index = -1
        for i in range(self.stacked_widget.count()):
            if isinstance(self.stacked_widget.widget(i), PrinterDetailsView):
                details_widget_index = i
                break

        if details_widget_index != -1:
            # Update existing view
            existing_view = self.stacked_widget.widget(details_widget_index)
            existing_view.label.setText(f"Printer Details for {printer_name} (ID: {printer_id})")
            self.stacked_widget.setCurrentIndex(details_widget_index)
        else:
            # Create and add new view
            new_details_view = PrinterDetailsView(printer_id=printer_id, parent=self)
            new_details_view.label.setText(f"Printer Details for {printer_name} (ID: {printer_id})") # Update label before showing
            details_widget_index = self.stacked_widget.addWidget(new_details_view)
            self.stacked_widget.setCurrentIndex(details_widget_index)

        self.statusBar.showMessage(f"Viewing details for printer: {printer_name}")


def main():
    app = QApplication(sys.argv)

    # Load and apply QSS stylesheet using resource_path
    qss_file_path = resource_path("static/css/dark_theme.qss")
    try:
        with open(qss_file_path, "r") as file:
            app.setStyleSheet(file.read())
            # print(f"INFO: Successfully loaded stylesheet from: {qss_file_path}") # Optional logging
    except FileNotFoundError:
        print(f"Warning: Stylesheet not found at: {qss_file_path}. Using default styles.")
    except Exception as e:
        print(f"Warning: Could not apply stylesheet from {qss_file_path}: {e}")

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
