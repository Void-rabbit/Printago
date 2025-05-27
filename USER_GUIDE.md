# 3D Print Farm Manager - User Guide

# Printago Manager - User Guide

## Introduction

Welcome to the Printago Manager! This desktop application aims to help you manage your 3D printing projects, with an initial focus on integrating with Bambu Lab Cloud services.

**Current State:** The application is in an early development stage. The primary functionality currently implemented is user authentication with Bambu Lab Cloud and an attempt to list your registered printers. Due to unconfirmed API endpoints for printer listing, this feature is **currently blocked** and may not display your printers. Advanced features described in UI mockups (like detailed printer control, job submission, etc.) are **not yet implemented** in the desktop UI.

## Getting Started

**Accessing the Application:**

*   **Desktop Application (`PrintagoManager.exe` or `PrintagoManager`):**
    *   If you are running a version built with PyInstaller (as described in `DEPLOYMENT.MD`), locate the executable (e.g., in the `dist/PrintagoManager` folder) and run it.
    *   If running from source: `python3 desktop_app.py`.
*   The application will open a desktop window.

## Authentication (Bambu Lab Cloud)

The application uses your Bambu Lab Cloud account for authentication.

*   **Logging In:**
    1.  On startup, or by clicking the "Login" button in the toolbar if you previously logged out, a login dialog will appear.
    2.  **Email:** Enter the email address associated with your Bambu Lab account.
    3.  **Password:** Enter your Bambu Lab account password.
    4.  Click "OK".
    5.  The application will attempt to authenticate. A status message will indicate success or failure.
    6.  If successful, the application will try to fetch your printer list.
*   **Token Storage:** Upon successful login, an authentication token is stored locally in a secure manner (in `~/.printago_manager/cloud_auth.json`). The application will attempt to use this token on subsequent startups to automatically log you in.
*   **Logging Out:**
    *   Click the "Logout" button in the toolbar. This will clear the locally stored authentication token. You will need to log in again to access cloud features.

## Main Application Window

The main window currently consists of:

*   **Toolbar:**
    *   **Printers:** Switches to the printer list view (default view).
    *   **Settings:** Switches to a placeholder settings view.
    *   **Logout:** Clears your saved Bambu Lab authentication token.
    *   **Login:** Allows you to log in if no valid token is present.
*   **Printer List View:**
    *   Displays a table intended to list your Bambu Lab Cloud registered printers.
    *   **Current Limitation:** Due to unconfirmed API endpoints, this list will likely appear empty or show an error message.
    *   **Refresh Printers List Button:** Attempts to re-fetch the printer list.
*   **Settings View (Placeholder):**
    *   This view is a placeholder for future application settings (e.g., theme selection, API key configurations for other services). Currently, it only contains basic UI elements.
*   **Status Bar:**
    *   Located at the bottom of the window.
    *   Displays messages about application status (e.g., "Ready.", "Authenticating...", "Login successful!", "Failed to fetch printers.").

## Planned/Unimplemented Features (from UI Mockups)

The following features were part of the initial UI design but are **not yet implemented** in the current desktop application due to development tool limitations encountered during the project:

*   **Detailed Printer View:**
    *   Tabbed interface for "Status & Controls", "Print Profiles", "Device Information".
    *   Real-time display of nozzle/bed temperatures, current job, print progress.
    *   Controls for Pause/Resume/Cancel print.
    *   Management of print profiles.
    *   Detailed device information.
    *   Initiating new print jobs from this view.
*   **Print Job Submission Screen:**
    *   File selection for G-code.
    *   Selection of target printer, print profiles, materials.
    *   Print job summary and start functionality.
*   **Advanced Settings:**
    *   Full theme selection.
    *   Configuration for Printago Store API (if this integration path is pursued).

## Flask Web Application & API (Separate Legacy Component)

The project also contains a Flask-based web application. This is a **separate component** and is not directly integrated into the current desktop UI's primary workflow. It was developed in earlier stages and features:

*   Its own user authentication system (using local JSON files, distinct from Bambu Lab Cloud).
*   Management of parts, printers (local data), and print jobs via a web interface.
*   A RESTful API for these entities.
*   To run the Flask web application: `python3 run.py` (or `app.py`) and access via `http://127.0.0.1:5000/`.
*   API documentation for this Flask API is available at `/api/docs` when the Flask app is running.

## For Developers: Using `printago_client.py`

A Python client for the **Printago API** (`printago_client.py`) has been developed based on their OpenAPI specification. This client is **not currently used by the desktop application UI**.

*   **Functionality:** Includes methods for most Printago API endpoints (parts, printers, print jobs, etc.).
*   **Usage:** Can be used independently in Python scripts for interacting with a Printago store if you have an API Key and Store ID.
*   **Setup:**
    1.  Ensure `requests` is installed (`pip install requests`).
    2.  Modify the `if __name__ == '__main__':` block in `printago_client.py` to provide your actual Printago API Key and Store ID.
    3.  Run the script directly (`python3 printago_client.py`) to test its methods (many example calls are commented out by default).
*   Refer to `printago_api_research.md` and the `printago_openapi.json` file for more details on the Printago API.

---
Thank you for using the Printago Manager. We appreciate your understanding of its current development stage and limitations.
