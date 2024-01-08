from django.contrib.auth.models import User
from . models import Note
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

class NoteTestCase(APITestCase):

    """
    Test suite for Note
    """
    def setUp(self):
        self.data = {
            "title": "Billy Smith",
            "content": "This is a test message",
            "owner": 0,
            "shared_with": []
        }
        self.url = "http://127.0.0.1:8000/api/notes/"

        self.user = User.objects.create_user(
            username='testuser1', 
            password='this_is_a_test',
            email='testuser1@test.com'
        )
        
        #The app uses token authentication
        self.token = Token.objects.create(user = self.user)
        self.client = APIClient()
        
        # We pass the token in all calls to the API
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_notes(self):

        data = self.data
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(Note.objects.get().title, "Billy Smith")

    def test_create_note_without_title(self):
        '''
        test NoteViewSet create method when title is not in data
        '''
        data = {
            "content": "This is a test message",
            "owner": 0,
            "shared_with": []
        }
        # data.pop("title")
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_note_when_title_equals_blank(self):
        '''
        test NoteViewSet create method when title is blank
        '''
        data = {
            "title": "",
            "content": "This is a test message",
            "owner": 0,
            "shared_with": []
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_notes(self):
        '''
        test NoteViewSet view method 
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_note_with_id(self):
        '''
        test NoteViewSet get note with id
        '''
        data = self.data
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()  # get the created note
        self.assertEqual(note.title, "Billy Smith")
        url = f"http://127.0.0.1:8000/api/notes/{note.id}/"  # use the note's id in the url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_note_with_id(self):
        '''
        test NoteViewSet put note with id
        '''
        # Create a note
        data = self.data
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()  # get the created note

        # Update the note
        updated_data = {"title": "Updated title"}
        url = f"http://127.0.0.1:8000/api/notes/{note.id}/"  # use the note's id in the url
        response = self.client.put(url, updated_data, format='json')

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated title")

    def test_delete_note_with_id(self):
        '''
        test NoteViewSet delete note with id
        '''
        # Create a note
        data = self.data
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()  # get the created note

        # Delete the note
        url = f"http://127.0.0.1:8000/api/notes/{note.id}/"  # use the note's id in the url
        response = self.client.delete(url)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 0)  # check that the note has been deleted
    
    def test_share_note_with_id(self):
        '''
        test NoteViewSet share note with id
        '''
        # Create a note
        data = self.data
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()  # get the created note

        # Create a user to share with
        user_to_share_with = User.objects.create_user(username='testuser2', password='12345')

        # Share the note
        share_data = {"user_to_share_with": user_to_share_with.id}
        url = f"http://127.0.0.1:8000/api/notes/{note.id}/share/"  # use the note's id in the url
        response = self.client.post(url, share_data, format='json')

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "Note shared successfully")
        self.assertTrue(user_to_share_with in note.shared_with.all())  # check that the note has been shared with the user

    def test_get_notes_with_query(self):
        '''
        test NoteViewSet get notes with query
        '''
        # Create a note
        data = self.data
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)

        # Search for the note
        query = {"q": "Billy Smith"}
        url = f"http://127.0.0.1:8000/api/search/"  # use the search url
        response = self.client.get(url, query)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Billy Smith")

    def test_get_notes_without_query(self):
        '''
        test NoteViewSet get notes without query
        '''
        # Search for the note without providing a query
        url = f"http://127.0.0.1:8000/api/search/"  # use the search url
        response = self.client.get(url)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "Please provide a search query")
