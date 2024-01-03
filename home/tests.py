from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Note

class NoteAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_note_list_create_endpoint(self):
        # Test creating a new note
        response = self.client.post('/api/notes', {'title': 'New Note', 'content': 'New Content'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test getting a list of notes
        response = self.client.get('/api/notes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming one note has been created

    def test_note_detail_endpoint(self):
        # Create a new note
        note = Note.objects.create(user=self.user, title='Test Note', content='Test Content')

        # Test getting a specific note
        response = self.client.get(f'/api/notes/{note.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], note.id)

        # Add more test cases for updating and deleting a note

    def test_note_share_endpoint(self):
        # Create a new note
        note = Note.objects.create(user=self.user, title='Test Note', content='Test Content')

        # Test sharing a note
        response = self.client.put(f'/api/notes/{note.id}/share', {'shared_with': ['user2', 'prabin']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Add more test cases for invalid sharing scenarios

    def test_note_search_endpoint(self):
        # Create some notes
        Note.objects.create(user=self.user, title='Search Note 1', content='Search Content 1')
        Note.objects.create(user=self.user, title='Search Note 2', content='Search Content 2')

        # Test searching for notes
        response = self.client.get('/api/search?q=Search')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming both notes match the search query

        # Add more test cases for different search scenarios
