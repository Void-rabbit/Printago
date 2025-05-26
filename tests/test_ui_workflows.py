from tests.base_test import BaseTestCase
from app import PARTS_FILE, PRINTERS_FILE # For verifying data persistence

class TestUiWorkflows(BaseTestCase):

    def test_home_page_loads(self):
        """Test that the home page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the 3D Print Farm Manager', response.data)

    def test_farm_dashboard_page_loads(self):
        """Test that the farm dashboard page loads."""
        response = self.client.get('/farm_dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Print Farm Dashboard', response.data)

    def test_api_docs_page_loads(self):
        """Test that the API documentation page loads."""
        response = self.client.get('/api/docs')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'API Documentation', response.data)

    def test_add_part_via_ui(self):
        """Test adding a part through the UI form."""
        # First, ensure the add part page loads
        response_get = self.client.get('/parts/add')
        self.assertEqual(response_get.status_code, 200)
        self.assertIn(b'Add New Part', response_get.data)

        # Simulate form submission
        # Note: File upload is not directly tested here for simplicity as it requires more setup.
        # We are testing the form submission logic assuming a file field might be empty or handled.
        part_data = {
            'name': 'UI Test Part',
            'material': 'PETG',
            'print_settings': '0.15mm layer height, 3 walls',
            # 'part_file': (io.BytesIO(b"dummy file content"), 'test.stl') # If testing file upload
        }
        response_post = self.client.post('/parts/add', data=part_data, follow_redirects=True,
                                         content_type='multipart/form-data') # Use multipart for file uploads
        
        self.assertEqual(response_post.status_code, 200) # Should redirect to parts list
        self.assertIn(b'Part added successfully!', response_post.data)
        self.assertIn(b'UI Test Part', response_post.data) # Check if new part is listed

        # Verify the part was saved to the file
        parts_in_file = self.load_json_data(PARTS_FILE)
        self.assertTrue(any(p['name'] == 'UI Test Part' for p in parts_in_file))

    def test_add_printer_via_ui(self):
        """Test adding a printer through the UI form."""
        # Ensure add printer page loads
        response_get = self.client.get('/printers/add')
        self.assertEqual(response_get.status_code, 200)
        self.assertIn(b'Add New Printer', response_get.data)

        # Simulate form submission
        printer_data = {
            'name': 'UI Test Printer',
            'model': 'Prusa MK4',
            'status': 'idle',
            'ip_address': '192.168.1.101',
            'serial_number': 'SNUI001',
            'access_code': 'ACUI001'
        }
        response_post = self.client.post('/printers/add', data=printer_data, follow_redirects=True)
        
        self.assertEqual(response_post.status_code, 200) # Should redirect to printers list
        self.assertIn(b'Printer added successfully!', response_post.data)
        self.assertIn(b'UI Test Printer', response_post.data) # Check if new printer is listed

        # Verify the printer was saved to the file
        printers_in_file = self.load_json_data(PRINTERS_FILE)
        self.assertTrue(any(p['name'] == 'UI Test Printer' for p in printers_in_file))

    def test_view_parts_list_page(self):
        """Test navigating to the parts list page."""
        response = self.client.get('/parts')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Parts Management', response.data)

    def test_view_printers_list_page(self):
        """Test navigating to the printers list page."""
        response = self.client.get('/printers')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Printer Management', response.data)

    def test_view_print_queue_page(self):
        """Test navigating to the print queue page."""
        response = self.client.get('/print_queue')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Print Queue', response.data)
        
    def test_add_print_job_page_loads(self):
        """Test that the add print job page loads, even with no parts/printers."""
        response = self.client.get('/print_queue/add')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add New Print Job', response.data)
        # This test implicitly checks that the page doesn't crash if parts/printers lists are empty.

if __name__ == '__main__':
    unittest.main()
