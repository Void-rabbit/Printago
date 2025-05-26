# 3D Print Farm Manager - User Guide

## Introduction

Welcome to the 3D Print Farm Manager! This application is designed to help you manage your 3D printing projects, including parts, printers, and print jobs, all from a simple web interface. It also provides an API for programmatic access and integration.

## Getting Started

**Accessing the Application:**

*   **Local Development:** If you are running the application locally for development, it typically runs on `http://127.0.0.1:5000/`. Open this URL in your web browser.
*   **Deployed Executable:** If you are running a version built with PyInstaller (as described in `DEPLOYMENT.md`), the application will also start a local server, usually at `http://127.0.0.1:5000/`.
*   **Hosted Instance:** If the application is deployed on a server, use the URL provided for that instance.

Upon first visit, you will likely be greeted by the home page with options to Sign Up or Login.

## Authentication

User accounts are required to access most features of the application.

*   **Signing Up:**
    1.  Navigate to the "Sign Up" page using the navigation bar.
    2.  Enter your desired username and password.
    3.  Click "Sign Up".
    4.  If successful, you will be redirected to the login page with a success message.
*   **Logging In:**
    1.  Navigate to the "Login" page.
    2.  Enter your registered username and password.
    3.  Click "Login".
    4.  If successful, you will be redirected to the home page (or a dashboard) and a success message will be displayed.
*   **Logging Out:**
    *   Currently, the application does not feature an explicit "Logout" button or session invalidation beyond closing the browser or the server stopping. For enhanced security in a multi-user environment, this would typically involve session management and a logout link.

## Navigation

The main sections of the application can be accessed via the navigation bar at the top of each page:

*   **Home:** The main landing page with quick links.
*   **Farm Dashboard:** Provides an overview of all printers and a summary of the print queue.
*   **Parts:** Manage your 3D model part files.
*   **Printers:** Manage your 3D printers.
*   **Print Queue:** View and manage the queue of print jobs.
*   **API Docs:** View documentation for the application's API.
*   **Login / Sign Up:** Links for authentication.

## Managing Parts

This section allows you to keep track of your 3D printable parts.

*   **Viewing Parts:**
    *   Navigate to the "Parts" section from the navigation bar.
    *   A list of all added parts will be displayed, showing their name, material, and filename.
    *   Click on a part's name to view its details.
*   **Adding a New Part (UI):**
    1.  Go to the "Parts" section.
    2.  Click the "Add New Part" link.
    3.  Fill in the form:
        *   **Part Name:** A descriptive name for your part.
        *   **Material:** The material the part is intended to be printed with (e.g., PLA, PETG, ABS).
        *   **Print Settings:** Any specific slicer or print settings (e.g., layer height, infill).
        *   **Part File:** Upload the 3D model file (e.g., STL, 3MF). (File upload is conceptual in the current UI for adding parts, the filename is stored).
    4.  Click "Add Part". You will be redirected to the parts list with a success message.
*   **Viewing Part Details:**
    *   From the parts list, click on a part's name.
    *   This page shows all stored information about the part.
    *   From here, you can also "Create Print Job with this Part".
*   **Managing Parts (API):**
    *   Parts can also be managed programmatically via the API. This allows for creating, viewing, updating, and deleting parts.
    *   API access requires an API key.
    *   Refer to the **API Documentation** (linked in the navigation bar or at `/api/docs`) for detailed instructions on using the `/api/parts` endpoints.

## Managing Printers

This section is for managing the 3D printers in your farm.

*   **Viewing Printers:**
    *   Navigate to the "Printers" section.
    *   A list of all added printers is displayed, showing their name, model, status, IP, and serial.
    *   Click on a printer's name to view its details.
*   **Adding a New Printer (UI):**
    1.  Go to the "Printers" section.
    2.  Click the "Add New Printer" link.
    3.  Fill in the form:
        *   **Printer Name:** A custom name for your printer (e.g., "Main Prusa", "Bambu X1C").
        *   **Printer Model:** The model of the printer (e.g., "Prusa MK3S+", "Bambu Lab X1 Carbon").
        *   **Status:** Initial status (e.g., Idle, Printing, Error).
        *   **IP Address:** The local network IP address of the printer (e.g., `192.168.1.100`).
        *   **Serial Number:** The printer's serial number. For Bambu Lab printers, this is found on the printer's touch screen (usually under Settings -> General). This is crucial for API interaction.
        *   **Access Code:** The printer's access code. For Bambu Lab printers, this is found on the printer's touch screen (usually under Settings -> Network). This is used as a password for local MQTT API access.
    4.  Click "Add Printer".
*   **Viewing Printer Details:**
    *   From the printers list, click on a printer's name.
    *   This page shows all stored information and a (currently mocked) live status (state, temperatures, progress).
    *   A placeholder for the camera feed is also present. For real integration, this would require the printer's IP address and potentially the access code.

## Managing Print Jobs

This section allows you to view and manage the queue of print jobs.

*   **Viewing the Print Queue:**
    *   Navigate to the "Print Queue" section.
    *   Jobs are listed, sorted by priority (lower numbers are higher priority, e.g., 0 is highest) and then by creation time.
    *   Each job shows its ID, part name, printer name, status, priority, and creation time.
    *   Click on a Job ID to view its details.
*   **Adding a New Print Job (UI):**
    1.  You can add a print job either from the "Print Queue" page by clicking "Add New Print Job", or from a specific part's detail page by clicking "Create Print Job with this Part".
    2.  Fill in the form:
        *   **Select Part:** Choose from the list of existing parts.
        *   **Select Printer:** Choose from the list of available printers.
        *   **Priority:** Assign a priority to the job. Lower numbers (e.g., 0, 1) mean higher priority. Default is 10.
    3.  Click "Add to Print Queue".
*   **Viewing Print Job Details:**
    *   From the print queue, click on a Job ID.
    *   This page shows detailed information about the job, including part and printer details, status, and timestamps.
*   **Bulk Actions (Conceptual):**
    *   On the Print Queue page, you can select multiple jobs using checkboxes.
    *   Buttons for "Cancel Selected Jobs" and "Move Selected to Top Priority" are available.
    *   **Note:** These bulk actions are currently conceptual. Clicking them will show an alert confirming the action and selected job IDs, but the backend logic for these operations is not yet implemented.

## Using the API

For advanced users or integration with other systems, the application provides a RESTful API.

*   **API Key:** All API endpoints require an `X-API-Key` header for authentication. The default key for development is `your_secret_api_key`.
*   **Documentation:** Full details for all API endpoints, including request/response formats and authentication, can be found on the **API Documentation** page, accessible from the navigation bar or by navigating directly to `/api/docs`.
*   **Current Capabilities:** The API currently supports:
    *   Full CRUD (Create, Read, Update, Delete) operations for Parts.
    *   Read-only operations for Printers and Print Jobs.

---
Thank you for using the 3D Print Farm Manager!
