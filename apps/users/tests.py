from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class AuthenticationApiTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user_data = {
			'email': 'user@example.com',
			'first_name': 'Test',
			'last_name': 'User',
			'password': 'pass12345',
		}

	def test_register_login_and_profile(self):
		register_response = self.client.post('/api/auth/register/', self.user_data, format='json')
		login_response = self.client.post(
			'/api/auth/login/',
			{'email': self.user_data['email'], 'password': self.user_data['password']},
			format='json',
		)

		self.assertEqual(register_response.status_code, 201)
		self.assertEqual(login_response.status_code, 200)
		self.assertIn('access', login_response.data)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}")

		profile_response = self.client.get('/api/auth/profile/')

		self.assertEqual(profile_response.status_code, 200)
		self.assertEqual(profile_response.data['email'], self.user_data['email'])

	def test_password_is_hashed(self):
		self.client.post('/api/auth/register/', self.user_data, format='json')
		user = get_user_model().objects.get(email=self.user_data['email'])

		self.assertNotEqual(user.password, self.user_data['password'])

# Create your tests here.
