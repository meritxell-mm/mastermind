from django.urls import path
from .views import NewGame, GuessCode


urlpatterns = [
    path('new', NewGame.as_view(), name="new_game"),
    path('guess_code', GuessCode.as_view(), name="guess_code")
]