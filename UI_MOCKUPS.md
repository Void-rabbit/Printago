# UI/UX Mockups & Descriptions for Printago Manager

**Disclaimer:** The mockups and descriptions below represent the *target design and feature set* for the Printago Manager desktop application. Due to development tool limitations encountered during the project, the current UI implemented in `desktop_app.py` is more basic and does not include all the features or the full visual fidelity detailed here. This document should be seen as a design goal for future development iterations.

## 1. Overall Theme and Principles

*   **Theme:**
    *   Predominantly dark theme (e.g., dark gray or charcoal backgrounds).
    *   Accent colors: "Printago blue" (if a specific brand blue exists) or a similar productive, modern blue/teal for highlights, buttons, and active states.
    *   Text: Light-colored text (white or light gray) for readability against the dark background.
*   **Font:**
    *   Clean, modern sans-serif font (e.g., Segoe UI, Roboto, Open Sans, or system default sans-serif).
*   **Layout:**
    *   Consistent spacing and alignment throughout the application.
    *   Clear visual hierarchy: Important elements should be more prominent.
    *   Intuitive navigation.
*   **Data Display:**
    *   Prioritize displaying essential and user-friendly information.
    *   Internal IDs (e.g., `part_id`, `job_id`) should generally be hidden by default in main views but accessible in detailed views or logs if needed.
    *   Use icons where appropriate to enhance visual communication (e.g., printer status, actions).
*   **Interactions:**
    *   Dropdowns (combo boxes) for selecting from a list of options (e.g., printers, print profiles).
    *   Clearly labeled buttons for actions.
    *   Tooltips for icons or less obvious controls.
    *   Feedback mechanisms (status messages, progress indicators).

## 2. Login Screen

*   **Window Title:** "Printago Manager Login"
*   **Layout:** Single, centered dialog or view.

*   **Primary Section: Bambu Lab Cloud Account Login (Main Focus)**
    *   **Title/Header:** "Connect your Bambu Lab Account"
    *   **Fields:**
        *   Email Input Field (Label: "Email:", Placeholder: "Enter your Bambu Lab email")
        *   Password Input Field (Label: "Password:", Placeholder: "Password", masked)
    *   **Controls:**
        *   "Remember Me" Checkbox (optional, consider security implications).
        *   "Login" Button (primary accent color).
        *   "Forgot Password?" Link (navigates to Bambu Lab's password reset page in a browser).
    *   **Helper Text:** (Optional) "Login with your Bambu Lab cloud credentials (email and password) to access your registered printers."

*   **Secondary/Alternative Section: Printago Store API Key Configuration (Placeholder/Advanced)**
    *   **Title/Header:** (Optional, could be under an "Advanced" or "Connect to Printago Store" expandable section if both logins are present on one screen. If separate, this would be its own view).
        "Connect to a Printago Store (Optional)"
    *   **Description:** "If you have a Printago Store API Key, enter it here to connect the manager to your store. This is separate from your Bambu Lab account."
    *   **Fields:**
        *   Printago API Key Input Field (placeholder: "Enter Printago API Key")
        *   Printago Store ID Input Field (placeholder: "Enter Printago Store ID")
    *   **Controls:**
        *   "Connect to Store" Button.

*   **Status Bar/Area:**
    *   Located at the bottom of the screen.
    *   Displays feedback messages (e.g., "Authenticating...", "Login failed: Invalid credentials", "Connected to Printago Store").

## 3. Main Window / Dashboard

*   **Window Title:** "Printago Manager - Dashboard"
*   **Navigation:**
    *   **Option A (Sidebar):** A vertical navigation panel on the left.
        *   Icons and text labels: "Dashboard", "Printers" (or "My Printers"), "Settings".
    *   **Option B (Top Navigation Bar):** A horizontal bar below the window title area.
        *   Text labels or icons for "Dashboard", "Printers", "Settings".
    *   User account display (e.g., "Logged in as: user@example.com") and a "Logout" button.

*   **Dashboard View (Default View after Login):**
    *   **Title:** "Printers Overview" or "My Cloud Printers"
    *   **Display Area:**
        *   **Layout:** Grid or list view for displaying printers.
        *   **Printer Card/Item:** Each printer representation should show:
            *   Printer Name (user-defined or fetched from cloud).
            *   Status Indicator (e.g., icon with color: Green for Idle/Ready, Blue for Printing, Yellow for Warning, Red for Error). Text status like "Printing - 67%".
            *   Printer Model or Icon representing the printer type.
            *   "View Details" Button (or clickable card) to navigate to the Printer Details View.
    *   **Overall Statistics (Optional):**
        *   Small section displaying stats like "Total Printers: 5", "Currently Printing: 2".
    *   **Controls:**
        *   "Refresh Printer List" Button (to fetch the latest printer list and statuses from the cloud).
        *   (Optional) "Add New Printer" if manual addition is supported alongside cloud discovery.

## 4. Printer Details View

*   **Window Title:** "[Printer Name] - Details | Printago Manager"
*   **Layout:**
    *   Header area displaying the Printer Name prominently.
    *   Tabbed interface or clearly separated sections for different categories of information.

*   **Section 1: Status & Controls (Default Tab/Top Section)**
    *   **Title:** "Live Status & Controls"
    *   **Status Display:**
        *   Nozzle Temperature: Current / Target (e.g., "220°C / 220°C")
        *   Bed Temperature: Current / Target (e.g., "60°C / 60°C")
        *   Current Job: Name of the G-code file or job ID being printed.
        *   Print Progress: Percentage, progress bar, or estimated time remaining.
        *   Camera Feed: Embedded view if available.
    *   **Controls:**
        *   "Pause Print" Button (enabled if printing).
        *   "Resume Print" Button (enabled if paused).
        *   "Cancel Print" Button (enabled if printing or paused, with confirmation dialog).

*   **Section 2: Print Profiles (Tab or Collapsible Section)**
    *   **Title:** "Print Profiles"
    *   **Display:**
        *   Dropdown or list view of available print profiles for this printer (fetched from cloud or local storage).
        *   Each profile shows its name and key settings summary.
    *   **Controls:**
        *   "View/Edit Selected Profile" Button.
        *   (Optional) "Create New Profile", "Import Profile".

*   **Section 3: Device Information (Tab or Collapsible Section)**
    *   **Title:** "Device Information"
    *   **Display (read-only fields):**
        *   Printer Model
        *   Serial Number
        *   Firmware Version
        *   IP Address (if applicable on local network)
        *   Cloud Connection Status

*   **Section 4: Job Submission (Tab or Prominent Button)**
    *   **Title/Button Label:** "Start New Print Job"
    *   This would navigate to the Print Job Submission Screen for this specific printer.

## 5. Print Job Submission Screen

*   **Window Title:** "Start New Print Job on [Printer Name] | Printago Manager"
*   **Layout:** Form-based layout.

*   **Fields & Controls:**
    *   **File Selection:**
        *   "Select G-code File" Button (opens a file dialog).
        *   Display area for the selected filename.
    *   **Target Printer:**
        *   Read-only display of the selected printer name (pre-filled from the context of navigation).
        *   (Or) Dropdown to select a printer if accessed generically.
    *   **Print Profile Selection:**
        *   Dropdown list of available print profiles compatible with the selected printer/material.
    *   **Material Type (Optional):**
        *   Dropdown to select material type if not implicitly part of the profile (e.g., PLA, PETG, ABS).
    *   **Presets/Overrides (Optional/Advanced):**
        *   Section for quick overrides like "Speed: Normal/Sport", "Infill: 15%/20%".
*   **Print Job Summary (Optional):**
    *   A small section that dynamically updates to show:
        *   Estimated Print Time (if calculable from G-code/profile).
        *   Estimated Material Usage.
*   **Action Buttons:**
    *   "Start Print" Button (primary accent color).
    *   "Cancel" or "Back to Printer Details" Button.

---
This textual mockup provides a foundational understanding of the UI. Visual design tools and prototyping would further refine these concepts.I have created the `UI_MOCKUPS.md` file with the specified content in the previous turn.
I will now submit the subtask report.
