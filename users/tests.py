from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class NoteAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_authentication_endpoints(self):
        client = APIClient()

        # Test user registration
        response = client.post('/api/auth/signup', {'username': 'newuser', 'password': 'newpass'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test user login
        response = client.post('/api/auth/login', {'username': 'newuser', 'password': 'newpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)