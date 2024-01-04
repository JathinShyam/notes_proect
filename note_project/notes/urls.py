from django.urls import path
from .views import LoginAPI, RegisterAPI, note, SignOutAPI, NotesAPI

urlpatterns = [
    path('auth/login/', LoginAPI.as_view()),
    path('auth/register/', RegisterAPI.as_view()),
    path('auth/logout/', SignOutAPI.as_view()),
    path('notes/', NotesAPI.as_view()),
    # path('notes/', note, name='note'),
]
