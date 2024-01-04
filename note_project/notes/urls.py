from django.urls import path
from .views import LoginAPI, RegisterAPI, SignOutAPI, NotesAPI, NoteDetailAPI, NoteShareAPI, NoteSearchAPI

urlpatterns = [
    path('auth/login/', LoginAPI.as_view()), # Login user
    path('auth/register/', RegisterAPI.as_view()), # Register user
    # path('auth/logout/', SignOutAPI.as_view()),
    path('notes/', NotesAPI.as_view()), # View or create notes
    path('notes/<int:id>/', NoteDetailAPI.as_view(), name='note-detail'), # View, update or delete a note
    path('notes/<int:id>/share/', NoteShareAPI.as_view(), name='note-share'), # Share a note
    path('search/', NoteSearchAPI.as_view(), name='note-search'), # Search notes
]
