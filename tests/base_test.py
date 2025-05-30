import unittest
import tempfile
import os
import json
from app import app, USERS_FILE, PARTS_FILE, PRINTERS_FILE, PRINT_JOBS_FILE, CONFIG_API_KEY

class BaseTestCase(unittest.TestCase):
    """A base test case for the Flask application."""

    def setUp(self):
        """Set up a test client and temporary data files."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing forms easily
        self.client = app.test_client()

        # Create temporary files for data storage
        self.temp_users_fd, app.config['USERS_FILE_PATH'] = tempfile.mkstemp(suffix='.json')
        self.temp_parts_fd, app.config['PARTS_FILE_PATH'] = tempfile.mkstemp(suffix='.json')
        self.temp_printers_fd, app.config['PRINTERS_FILE_PATH'] = tempfile.mkstemp(suffix='.json')
        self.temp_print_jobs_fd, app.config['PRINT_JOBS_FILE_PATH'] = tempfile.mkstemp(suffix='.json')

        # Initialize temp files with empty data
        self.init_temp_json_file(app.config['USERS_FILE_PATH'], {}) # Users is a dict
        self.init_temp_json_file(app.config['PARTS_FILE_PATH'], [])
        self.init_temp_json_file(app.config['PRINTERS_FILE_PATH'], [])
        self.init_temp_json_file(app.config['PRINT_JOBS_FILE_PATH'], [])

        # Override the global file paths in app module to use temp files
        global USERS_FILE, PARTS_FILE, PRINTERS_FILE, PRINT_JOBS_FILE
        self.original_users_file = USERS_FILE
        self.original_parts_file = PARTS_FILE
        self.original_printers_file = PRINTERS_FILE
        self.original_print_jobs_file = PRINT_JOBS_FILE

        USERS_FILE = app.config['USERS_FILE_PATH']
        PARTS_FILE = app.config['PARTS_FILE_PATH']
        PRINTERS_FILE = app.config['PRINTERS_FILE_PATH']
        PRINT_JOBS_FILE = app.config['PRINT_JOBS_FILE_PATH']

        self.api_key = CONFIG_API_KEY
        self.headers = {
            'X-API-Key': self.api_key
        }


    def tearDown(self):
        """Clean up temporary files and restore original file paths."""
        os.close(self.temp_users_fd)
        os.close(self.temp_parts_fd)
        os.close(self.temp_printers_fd)
        os.close(self.temp_print_jobs_fd)

        os.unlink(app.config['USERS_FILE_PATH'])
        os.unlink(app.config['PARTS_FILE_PATH'])
        os.unlink(app.config['PRINTERS_FILE_PATH'])
        os.unlink(app.config['PRINT_JOBS_FILE_PATH'])

        global USERS_FILE, PARTS_FILE, PRINTERS_FILE, PRINT_JOBS_FILE
        USERS_FILE = self.original_users_file
        PARTS_FILE = self.original_parts_file
        PRINTERS_FILE = self.original_printers_file
        PRINT_JOBS_FILE = self.original_print_jobs_file

    def init_temp_json_file(self, filepath, data):
        """Helper to initialize a JSON file with data."""
        with open(filepath, 'w') as f:
            json.dump(data, f)

    def load_json_data(self, filepath):
        """Helper to load data from a JSON file."""
        with open(filepath, 'r') as f:
            return json.load(f)

if __name__ == '__main__':
    unittest.main()
