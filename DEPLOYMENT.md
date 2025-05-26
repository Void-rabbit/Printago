# Deploying the 3D Print Farm Manager as an Installable Application

This document provides instructions on how to build a standalone executable for the 3D Print Farm Manager application using PyInstaller. It also includes notes on the nature of this type of deployment.

## Building the Executable

Follow these steps to build the executable:

1.  **Set up your Python Environment:**
    *   Ensure you have Python 3 installed.
    *   It is highly recommended to create a virtual environment for the project to manage dependencies cleanly.
        ```bash
        python3 -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate
        ```

2.  **Install Dependencies:**
    *   With your virtual environment activated, install all required dependencies from `requirements.txt`. This includes PyInstaller.
        ```bash
        pip install -r requirements.txt
        ```

3.  **Run PyInstaller:**
    *   Navigate to the root directory of the project (where `app.spec` and `run.py` are located).
    *   Run PyInstaller using the provided `app.spec` file:
        ```bash
        pyinstaller app.spec
        ```
    *   PyInstaller will analyze the application, collect all necessary files, and build the executable. This process might take a few minutes.

4.  **Find the Output:**
    *   Once PyInstaller has finished, you will find the output in a directory named `dist` within your project root.
    *   Inside `dist/PrintFarmManager` (or `dist/run` if the name in the spec file wasn't customized fully), you will find the executable file (e.g., `PrintFarmManager.exe` on Windows, or `PrintFarmManager` on macOS/Linux) along with other necessary files and folders (like `templates`, `static`, and your JSON data files).

## Running the Application

1.  Navigate to the output directory (e.g., `dist/PrintFarmManager`).
2.  Run the executable (`PrintFarmManager.exe` or `PrintFarmManager`).
3.  A console window will open (as configured in `app.spec`), and it will show Flask's development server starting up.
4.  Open your web browser and navigate to `http://127.0.0.1:5000`.
5.  You should see the 3D Print Farm Manager application running.

## Nature of this "Installable App"

*   **Bundled Web Application:** The generated executable is essentially the Flask web application bundled together with a Python interpreter and all its dependencies.
*   **Local Web Server:** When you run the executable, it starts a local web server on your machine (listening on `http://127.0.0.1:5000` by default as configured in `run.py`).
*   **Browser Access:** To use the application, you need to open a web browser and go to the local server's address. It does not automatically open a native GUI window in the way a traditional desktop application might.
*   **Not a Native GUI:** This approach is different from creating a native desktop application with frameworks like PyQt, Kivy (for Python), or Electron (for web technologies). Those frameworks are designed to build applications with their own dedicated windows and user interfaces, rather than relying on a separate web browser.
*   **Data Files:** The `users.json`, `parts.json`, `printers.json`, and `print_jobs.json` files are included alongside the executable. The application reads from and writes to these files in the same directory where the executable is located.

## Cross-Platform Challenges

*   **Platform-Specific Builds:** An executable built on one operating system (e.g., Windows) will generally not run on another (e.g., macOS or Linux).
*   **Separate Builds Needed:** To provide executables for multiple platforms, you would need to run PyInstaller on each target platform. For example, build the `.exe` on a Windows machine, the macOS app bundle on a macOS machine, and the Linux executable on a Linux machine.

## Debugging Notes

*   The `app.spec` file is configured with `console=True`. This means a command prompt or terminal window will appear when you run the application, showing logs and potential error messages from the Flask server. This is useful for debugging.
*   For a more "production-like" feel where the console window is hidden, you can change `console=True` to `console=False` and `windowed=True` to `windowed=True` in `app.spec` and rebuild. However, if errors occur, they might not be visible to the user without checking log files (if logging is implemented).
