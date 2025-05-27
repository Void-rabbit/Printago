# Deploying the Printago Manager Desktop Application

This document provides instructions on how to build a standalone executable for the **Printago Manager desktop application** using PyInstaller.

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
    *   With your virtual environment activated, install all required dependencies from `requirements.txt`. This includes PyInstaller and PySide2.
        ```bash
        pip install -r requirements.txt
        ```

3.  **Run PyInstaller:**
    *   Navigate to the root directory of the project (where `app.spec` and `desktop_app.py` are located).
    *   Run PyInstaller using the provided `app.spec` file:
        ```bash
        pyinstaller app.spec
        ```
    *   PyInstaller will analyze the application, collect all necessary files (including PySide2 components), and build the executable. This process might take a few minutes.

4.  **Find the Output:**
    *   Once PyInstaller has finished, you will find the output in a directory named `dist` within your project root.
    *   Inside `dist/PrintagoManager` (or `dist/desktop_app` if the name in the spec file wasn't customized fully), you will find the executable file (e.g., `PrintagoManager.exe` on Windows, or `PrintagoManager` on macOS/Linux) along with other necessary files and folders.

## Running the Application

1.  Navigate to the output directory (e.g., `dist/PrintagoManager`).
2.  Run the executable (`PrintagoManager.exe` or `PrintagoManager`).
3.  The Printago Manager desktop application window should appear.

## Nature of the Desktop Application

*   **Native Desktop GUI:** The generated executable is a native desktop application built using PySide2 (Qt for Python). It runs in its own window and does not require a separate web browser.
*   **Bundled Dependencies:** PyInstaller bundles the Python interpreter, PySide2 libraries, and other necessary dependencies into the executable or its accompanying folder.
*   **Data Files (If Flask Backend is Used):** If the desktop application still interacts with the Flask backend (e.g., for API calls using `app.py`), the `app.spec` file is configured to bundle the JSON data files (`users.json`, `parts.json`, etc.) and Flask templates/static files. The interaction between the desktop UI and the Flask backend needs to be clearly defined (e.g., Flask running as a local server that the desktop app communicates with).
    *   If the desktop app evolves to handle data independently (e.g., local SQLite database or direct cloud API calls), the need to bundle these Flask-specific data files and components might diminish. The current `app.spec` is configured to bundle the Flask components as `desktop_app.py` imports from `app.py` (though this link might be vestigial if Flask is not actively serving content to the desktop UI).
    *   **Current UI State:** The packaged application will reflect the basic UI state of `desktop_app.py`, which includes login functionality for Bambu Lab Cloud and a printer list display that is likely non-functional due to API endpoint uncertainties. Advanced UI features from mockups are not present.

## Cross-Platform Challenges

*   **Platform-Specific Builds:** An executable built on one operating system (e.g., Windows) will generally not run on another (e.g., macOS or Linux).
*   **Separate Builds Needed:** To provide executables for multiple platforms, you would need to run PyInstaller on each target platform. For example, build the `.exe` on a Windows machine, the macOS app bundle (using the `BUNDLE` command in the spec file) on a macOS machine, and the Linux executable on a Linux machine.

## Debugging Notes

*   The `app.spec` file is currently configured with `console=True` and `windowed=False`. This means a command prompt or terminal window will appear when you run the application, which can be helpful for seeing `print` statements or error messages from the PySide2 application during development and debugging.
*   For a release version where the console is not desired, change `console=True` to `console=False` and `windowed=True` in `app.spec` before building.
*   Ensure that all necessary PySide2 plugins (e.g., platform plugins) are correctly collected by PyInstaller. The `collect_data_files('PySide2', include_py_files=True)` line in `app.spec` helps with this.
*   The `app.spec` file also includes Flask-related data files and hidden imports because `desktop_app.py` currently imports from `app.py` (even if the Flask server itself isn't the primary interface). If `desktop_app.py` were made fully independent of `app.py` imports, these could be removed from the spec file for a smaller package.
