# from app import app # Commented out to prevent Flask app import

if __name__ == '__main__':
    print("INFO: This script (run.py) is intended for running the Flask web server directly.")
    print("INFO: The desktop application should be launched using 'desktop_app.py'.")
    print("INFO: PyInstaller should use 'desktop_app.py' as its entry point.")
    
    # To prevent accidental Flask server start if this script is run:
    # Option 1: Comment out the app.run() call
    # app.run(host='127.0.0.1', port=5000, debug=False)
    
    # Option 2: Define it in a function that isn't called
    # def run_flask_server():
    #     from app import app # Import here to avoid loading if not called
    #     print("WARNING: run.py is executing app.run() for Flask!")
    #     # For a self-contained desktop app feel, running on 127.0.0.1 is typical.
    #     # Port 5000 is standard for Flask development.
    #     # debug=False is important for a "production" bundled app.
    #     app.run(host='127.0.0.1', port=5000, debug=False)
    
    # if False: # Ensure run_flask_server is not called by default
    #    run_flask_server()
    
    print("INFO: Exiting run.py without starting Flask server.")
