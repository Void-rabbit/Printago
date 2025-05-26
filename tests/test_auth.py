import json
from tests.base_test import BaseTestCase
from app import USERS_FILE, bcrypt # Import bcrypt to verify password hashes if needed

class TestAuth(BaseTestCase):

    def test_signup_page_loads(self):
        """Test that the signup page loads correctly."""
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)

    def test_successful_signup(self):
        """Test successful user signup."""
        response = self.client.post('/signup', data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200) # After redirect to login
        self.assertIn(b'Signup successful! Please login.', response.data)
        
        # Verify user is in the users file
        users_data = self.load_json_data(USERS_FILE)
        self.assertIn('testuser', users_data)
        # Optionally, verify the password hash
        self.assertTrue(bcrypt.checkpw('testpassword'.encode('utf-8'), users_data['testuser'].encode('utf-8')))

    def test_signup_existing_user(self):
        """Test signup with an already existing username."""
        # First, create a user
        self.client.post('/signup', data={
            'username': 'existinguser',
            'password': 'password123'
        }, follow_redirects=True)

        # Try to sign up again with the same username
        response = self.client.post('/signup', data={
            'username': 'existinguser',
            'password': 'anotherpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200) # Stays on signup page (or redirects to signup)
        self.assertIn(b'Username already exists!', response.data)

    def test_login_page_loads(self):
        """Test that the login page loads correctly."""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_successful_login(self):
        """Test successful user login."""
        # First, sign up a user
        self.client.post('/signup', data={
            'username': 'loginuser',
            'password': 'loginpassword'
        }, follow_redirects=True) # Redirects to login page

        # Now, log in
        response = self.client.post('/login', data={
            'username': 'loginuser',
            'password': 'loginpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200) # Assuming redirect to home/dashboard
        self.assertIn(b'Login successful!', response.data) 
        # Check if it redirected to the home page (or a dashboard if that's the target)
        self.assertIn(b'Welcome to the 3D Print Farm Manager', response.data)


    def test_login_incorrect_username(self):
        """Test login with an incorrect username."""
        self.client.post('/signup', data={'username': 'realuser', 'password': 'realpassword'})
        response = self.client.post('/login', data={
            'username': 'fakeuser',
            'password': 'realpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200) # Stays on login page
        self.assertIn(b'Invalid username or password!', response.data)

    def test_login_incorrect_password(self):
        """Test login with an incorrect password."""
        self.client.post('/signup', data={'username': 'userpass', 'password': 'correctpass'})
        response = self.client.post('/login', data={
            'username': 'userpass',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200) # Stays on login page
        self.assertIn(b'Invalid username or password!', response.data)

    # Logout is not explicitly implemented as a route with session management in the current app
    # If session management (e.g., Flask-Login) were added, a /logout route test would go here.
    # For now, we'll skip a dedicated logout test.
    # def test_logout(self):
    #     """Test user logout."""
    #     # Login first
    #     self.client.post('/signup', data={'username': 'logoutuser', 'password': 'logoutpassword'})
    #     self.client.post('/login', data={'username': 'logoutuser', 'password': 'logoutpassword'}, follow_redirects=True)
        
    #     response = self.client.get('/logout', follow_redirects=True) # Assuming /logout exists and redirects
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'You have been logged out.', response.data) # Or similar message
    #     # Check that accessing a protected page redirects to login
    #     # response_protected = self.client.get('/dashboard', follow_redirects=True) 
    #     # self.assertIn(b'Please log in to access this page', response_protected.data)

if __name__ == '__main__':
    unittest.main()
