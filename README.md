# 3D Print Farm Manager

## Project Overview

The 3D Print Farm Manager is a web application designed to help users manage their 3D printing projects. It allows for tracking of 3D printable parts, managing a fleet of 3D printers, and organizing a queue of print jobs. The application provides a user-friendly web interface and a RESTful API for programmatic access and integration.

## Features

*   **User Authentication:** Secure signup and login for users.
*   **Part Management:**
    *   Store and manage a library of 3D printable parts (name, material, print settings, filename).
    *   Add new parts via UI.
    *   View part details.
*   **Printer Management:**
    *   Register and manage multiple 3D printers (name, model, status, IP address, serial number, access code).
    *   View printer details, including (mocked) live status and a placeholder for camera feeds.
*   **Print Queue Management:**
    *   Create and manage a queue of print jobs.
    *   Assign parts to specific printers.
    *   Job prioritization (lower numbers indicate higher priority).
    *   View job details and status.
    *   Conceptual bulk actions (cancel, prioritize) on the queue.
*   **Print Farm Dashboard:**
    *   Centralized overview of all registered printers and their (mocked) live status.
    *   Summary of the print queue (total jobs, pending, printing, completed, error).
*   **RESTful API:**
    *   Read-only access to parts, printers, and print jobs.
    *   Full CRUD (Create, Read, Update, Delete) operations for Parts.
    *   Basic API key authentication (`X-API-Key` header).
    *   Dedicated API documentation page.
*   **Web-Based UI:**
    *   User-friendly interface built with Flask and HTML templates.
    *   CSS styling for improved look and feel.
    *   Responsive design considerations for different screen sizes.
*   **Testing:**
    *   Unit tests for API endpoints, authentication logic, and basic UI workflows.
*   **Deployment Ready (Conceptual):**
    *   Includes PyInstaller setup for bundling the application as a standalone executable.

## Project Structure

*   `app.py`: Main Flask application file containing routes, business logic, and data handling.
*   `run.py`: Entry point for running the application, especially when bundled with PyInstaller.
*   `requirements.txt`: List of Python dependencies for the project.
*   `static/`: Directory for static assets (CSS, JavaScript, images).
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
*   `bambu_api_research.md`: Research notes on Bambu Lab printer APIs (for future integration).

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

There are a couple of ways to run the Flask development server:

*   **Using `python app.py` (if `app.run()` is present for development):**
    The `app.py` file is currently set up for this.
    ```bash
    python3 app.py
    ```
    The application will typically be available at `http://127.0.0.1:5000/`.

*   **Using `flask run`:**
    You might need to set the `FLASK_APP` environment variable first if your main app file is not `app.py` or `wsgi.py`.
    ```bash
    export FLASK_APP=app.py # On Windows: set FLASK_APP=app.py
    export FLASK_DEBUG=1    # Optional: enables debug mode
    flask run
    ```
    Or, more directly if your main file is `app.py`:
    ```bash
    flask run --debug
    ```
    The application will typically be available at `http://127.0.0.1:5000/`.

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

## API Documentation

The application provides a RESTful API. Documentation for the API, including endpoint details, authentication, and request/response formats, can be found at the `/api/docs` route when the application is running. (e.g., `http://127.0.0.1:5000/api/docs`).

---
