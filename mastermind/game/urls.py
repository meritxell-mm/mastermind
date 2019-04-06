from django.urls import path
from .views import NewGame, GuessCode
from rest_framework.generics import ListCreateAPIView

urlpatterns = [
    path('new', NewGame.as_view(), name="new_game"),
    path('guess', GuessCode.as_view(), name="guess"),
]