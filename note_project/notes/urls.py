from django.urls import path
from .views import LoginAPI, RegisterAPI

urlpatterns = [
    path('auth/login/', LoginAPI.as_view()),
    path('auth/register/', RegisterAPI.as_view()),
]
