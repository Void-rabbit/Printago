# 3D Print Farm Manager

## Project Overview

The 3D Print Farm Manager is a project that aimed to evolve into a desktop application for managing 3D printing projects, with an initial focus on Bambu Lab Cloud integration. The current version features a basic PySide2 desktop UI capable of user authentication against Bambu Lab Cloud and attempting to list registered printers. However, critical API endpoint information for listing printers remains unconfirmed, significantly limiting this core functionality. The application also includes a foundational Flask web backend with a RESTful API (for parts, printers, print jobs) and data storage via JSON files, which is currently separate from the desktop UI's functionality.

## Features

*   **Desktop Application (PySide2 - Current Focus):**
    *   User authentication with Bambu Lab Cloud API (username/password).
    *   Secure local storage and loading of authentication tokens.
    *   Basic UI for login, displaying a list of printers, and status messages.
    *   Attempted printer discovery via Bambu Lab Cloud API.
    *   **Limitation:** Printer list functionality is currently **blocked** due to unconfirmed API endpoints for fetching device lists post-authentication. The UI will likely show an empty printer list or an error.
    *   **Limitation:** The desktop UI is basic due to development tool limitations impacting UI construction. Advanced features like detailed printer views, job submission, and settings management as described in mockups are **not implemented** in the desktop app.
*   **Flask Web Application & API (Legacy/Separate Functionality):**
    *   User Authentication (separate from Bambu Cloud, uses local JSON file).
    *   Part Management (CRUD via UI and API).
    *   Printer Management (CRUD via UI - local data, no actual printer control).
    *   Print Queue Management (CRUD via UI - local data).
    *   Print Farm Dashboard (UI).
    *   RESTful API with API key authentication for parts, printers, and print jobs (as documented in `/api/docs` when the Flask app is running).
*   **Printago API Client:**
    *   A Python client (`printago_client.py`) for interacting with the Printago API (based on provided OpenAPI spec) has been developed, including read-only and CRUD methods. This is currently not integrated into any UI.
*   **Testing:**
    *   Unit tests for the Flask web application's API endpoints and authentication logic.
*   **Deployment Configuration:**
    *   PyInstaller setup (`app.spec`) configured for building the PySide2 `desktop_app.py` as a standalone executable.

## Project Structure

*   `app.py`: Main Flask application file containing routes, business logic, and data handling.
*   `desktop_app.py`: Main entry point for the PySide2 desktop application.
*   `app.py`: Main Flask application file (currently provides web UI and API, may transition to a backend service).
*   `run.py`: Original entry point for the Flask web application (its role may change).
*   `requirements.txt`: List of Python dependencies for the project.
*   `static/`: Directory for static assets (CSS, JavaScript, images) for the web interface.
    *   `static/css/style.css`: Main stylesheet for the application.
*   `templates/`: Directory for HTML templates used by Flask.
    *   `templates/base.html`: Base template providing common layout and navigation.
*   `users.json`, `parts.json`, `printers.json`, `print_jobs.json`: JSON files used for data storage (located in the project root).
*   `tests/`: Directory containing unit tests.
    *   `tests/base_test.py`: Base test case setup.
    *   `tests/test_api.py`: API tests.
    *   `tests/test_auth.py`: Authentication tests.
    *   `tests/test_ui_workflows.py`: UI workflow tests.
*   `run_tests.sh`: Shell script to execute all unit tests.
*   `app.spec`: PyInstaller specification file for building the executable.
*   `README.md`: This file - developer documentation.
*   `USER_GUIDE.md`: User manual for the application.
*   `DEPLOYMENT.MD`: Instructions for building and deploying the application as a standalone executable.
*   `bambu_api_research.md`: Research notes on Bambu Lab printer APIs (Local MQTT & Cloud Account API).
*   `printago_api_research.md`: Research notes on Printago API (Store-specific API).

## Development Setup

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create and Activate a Virtual Environment:**
    It is highly recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application (Development)

The primary focus for execution is the PySide2 desktop application:
```bash
python3 desktop_app.py
```
This will launch the desktop UI. Login with your Bambu Lab Cloud credentials. Note the known limitation regarding printer list display.

The Flask web application (for legacy UI and API) can be run separately if needed:
```bash
python3 run.py
```
Or using Flask CLI:
```bash
export FLASK_APP=app.py # On Windows: set FLASK_APP=app.py
export FLASK_DEBUG=1    # Optional: enables debug mode
flask run
```
The Flask app will be available at `http://127.0.0.1:5000/`.

## Running Tests

To run the automated test suite:

1.  Ensure all development dependencies are installed (including any test-specific libraries, though none are separate in this project).
2.  Make the `run_tests.sh` script executable (if needed):
    ```bash
    chmod +x run_tests.sh
    ```
3.  Execute the script from the project root directory:
    ```bash
    ./run_tests.sh
    ```
    Alternatively, you can run unittest discovery directly:
    ```bash
    python3 -m unittest discover -s tests -p "test_*.py"
    ```

## Building for Deployment

For instructions on how to build the application into a standalone executable using PyInstaller, please refer to [DEPLOYMENT.MD](./DEPLOYMENT.MD).

## User Guide

For instructions on how to use the application, its features, and workflows, please refer to the [USER_GUIDE.MD](./USER_GUIDE.MD).

## API Research & Integration Notes

For details on integrating with third-party printer APIs:
*   Bambu Lab Printers: See [bambu_api_research.md](./bambu_api_research.md) for information on both local MQTT and cloud-based API interactions. **Note the current blocker regarding printer list endpoints.**
*   Printago Service: See [printago_api_research.md](./printago_api_research.md) for information on their store-specific API (not integrated into UI).

## API Documentation (Flask Web Application)

The Flask web application provides a RESTful API. Documentation for this API, including endpoint details, authentication, and request/response formats, can be found at the `/api/docs` route when the Flask application is running (e.g., `http://127.0.0.1:5000/api/docs`).

---
