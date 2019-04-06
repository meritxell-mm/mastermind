from django.urls import path, re_path
from .views import NewGame, GuessCode, GuessList

urlpatterns = [
    path('new/', NewGame.as_view(), name="new_game"),
    path('guess/', GuessCode.as_view(), name="guess"),
    re_path('historic/(?P<game>\d+)/', GuessList.as_view(), name="historic")
]