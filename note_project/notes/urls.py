from django.urls import path
from .views import LoginAPI, RegisterAPI, SignOutAPI, NotesAPI, NoteDetailAPI, NoteShareAPI, NoteSearchAPI

urlpatterns = [
    path('auth/login/', LoginAPI.as_view()),
    path('auth/register/', RegisterAPI.as_view()),
    path('auth/logout/', SignOutAPI.as_view()),
    path('notes/', NotesAPI.as_view()),
    path('notes/<int:id>/', NoteDetailAPI.as_view(), name='note-detail'),
    path('notes/<int:id>/share/', NoteShareAPI.as_view(), name='note-share'),
    path('search/', NoteSearchAPI.as_view(), name='note-search'),
]
