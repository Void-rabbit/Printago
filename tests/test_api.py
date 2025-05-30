import json
from tests.base_test import BaseTestCase
from app import PARTS_FILE # To directly check the file content

class TestApiAuthentication(BaseTestCase):

    def test_missing_api_key(self):
        """Test API access with a missing API key."""
        response = self.client.get('/api/parts')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Missing API Key', response.get_json()['error']) # Updated expected error message based on current implementation

    def test_incorrect_api_key(self):
        """Test API access with an incorrect API key."""
        headers = {'X-API-Key': 'this-is-not-the-key'}
        response = self.client.get('/api/parts', headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid or missing API Key', response.get_json()['error'])

    def test_correct_api_key_for_get_parts(self):
        """Test API access with a correct API key for GET /api/parts."""
        response = self.client.get('/api/parts', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        # Further checks for data can be added here if needed

class TestPartsApi(BaseTestCase):

    def test_get_parts_empty(self):
        """Test GET /api/parts when no parts exist."""
        response = self.client.get('/api/parts', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_create_part_success(self):
        """Test POST /api/parts to create a new part successfully."""
        part_data = {
            "name": "Test Screw",
            "material": "PLA",
            "filename": "screw_v1.stl",
            "print_settings": "0.2mm layer height"
        }
        response = self.client.post('/api/parts', headers=self.headers, json=part_data)
        self.assertEqual(response.status_code, 201)
        created_part = response.get_json()
        self.assertIn('part_id', created_part)
        self.assertEqual(created_part['name'], part_data['name'])

        # Verify it's saved in the file
        parts_in_file = self.load_json_data(PARTS_FILE)
        self.assertEqual(len(parts_in_file), 1)
        self.assertEqual(parts_in_file[0]['name'], part_data['name'])

    def test_create_part_missing_fields(self):
        """Test POST /api/parts with missing required fields."""
        part_data = {"name": "Test Incomplete Part"} # Missing material
        response = self.client.post('/api/parts', headers=self.headers, json=part_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required fields', response.get_json()['error'])

    def test_get_specific_part_success(self):
        """Test GET /api/parts/<part_id> for an existing part."""
        # First, create a part
        part_data = {"name": "Widget", "material": "ABS"}
        post_response = self.client.post('/api/parts', headers=self.headers, json=part_data)
        part_id = post_response.get_json()['part_id']

        # Test getting the part
        response = self.client.get(f'/api/parts/{part_id}', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], part_data['name'])

    def test_get_specific_part_not_found(self):
        """Test GET /api/parts/<part_id> for a non-existent part."""
        response = self.client.get('/api/parts/non_existent_id', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Part not found', response.get_json()['error'])

    def test_update_part_success(self):
        """Test PUT /api/parts/<part_id> to update an existing part."""
        # Create a part
        part_data = {"name": "Old Name", "material": "PLA"}
        post_response = self.client.post('/api/parts', headers=self.headers, json=part_data)
        part_id = post_response.get_json()['part_id']

        # Update the part
        update_data = {"name": "New Name", "material": "PETG"}
        response = self.client.put(f'/api/parts/{part_id}', headers=self.headers, json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_part = response.get_json()
        self.assertEqual(updated_part['name'], "New Name")
        self.assertEqual(updated_part['material'], "PETG")

        # Verify change in file
        parts_in_file = self.load_json_data(PARTS_FILE)
        self.assertEqual(parts_in_file[0]['name'], "New Name")

    def test_update_part_not_found(self):
        """Test PUT /api/parts/<part_id> for a non-existent part."""
        update_data = {"name": "New Name"}
        response = self.client.put('/api/parts/non_existent_id', headers=self.headers, json=update_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Part not found', response.get_json()['error'])

    def test_delete_part_success(self):
        """Test DELETE /api/parts/<part_id> for an existing part."""
        # Create a part
        part_data = {"name": "To Be Deleted", "material": "PLA"}
        post_response = self.client.post('/api/parts', headers=self.headers, json=part_data)
        part_id = post_response.get_json()['part_id']

        parts_in_file = self.load_json_data(PARTS_FILE)
        self.assertEqual(len(parts_in_file), 1)

        # Delete the part
        response = self.client.delete(f'/api/parts/{part_id}', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Part deleted successfully', response.get_json()['message'])

        # Verify it's removed from the file
        parts_in_file_after_delete = self.load_json_data(PARTS_FILE)
        self.assertEqual(len(parts_in_file_after_delete), 0)

    def test_delete_part_not_found(self):
        """Test DELETE /api/parts/<part_id> for a non-existent part."""
        response = self.client.delete('/api/parts/non_existent_id', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Part not found', response.get_json()['error'])

class TestPrintersApi(BaseTestCase):

    def test_get_printers_empty(self):
        """Test GET /api/printers when no printers exist."""
        response = self.client.get('/api/printers', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_get_specific_printer_not_found(self):
        """Test GET /api/printers/<printer_id> for a non-existent printer."""
        response = self.client.get('/api/printers/non_existent_id', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Printer not found', response.get_json()['error'])

    # Note: More tests can be added here once printers can be created via API or UI in tests

class TestPrintJobsApi(BaseTestCase):

    def test_get_print_jobs_empty(self):
        """Test GET /api/print_jobs when no jobs exist."""
        response = self.client.get('/api/print_jobs', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_get_specific_print_job_not_found(self):
        """Test GET /api/print_jobs/<job_id> for a non-existent job."""
        response = self.client.get('/api/print_jobs/non_existent_id', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Print job not found', response.get_json()['error'])

    # Note: More tests can be added here once jobs can be created via API or UI in tests
    # and also to test the sorting and augmentation of job data.
if __name__ == '__main__':
    unittest.main()
