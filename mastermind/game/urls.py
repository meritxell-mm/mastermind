from django.urls import path
from .views import NewGame


urlpatterns = [
    path('new/', NewGame.as_view(), name="new_game")
]