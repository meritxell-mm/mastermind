from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Game
from .serializers import GameSerializer
from django.shortcuts import get_object_or_404


class CreateGame(APITestCase):
    response = None
    expected_obj = None

    def setUp(self):
        super().setUp()
        # API endpoint
        self.response = self.client.post(
            reverse("new_game")
        )
        # fetch db data
        self.expected_obj = Game.objects.all()[0]

    def test_create_game(self):
        """
        Ensures that api response is the game id
        when a POST request is made to the game/api/new
        """
        # check api response
        expected_data = GameSerializer(self.expected_obj)
        self.assertEqual(self.response.data, expected_data.data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_create_secret_code(self):
        """
        Ensures that a game is created with a secret_code
        when a POST request is made to the game/api/new
        """
        # check object values
        self.assertTrue(self.expected_obj)
        self.assertEqual(len(self.expected_obj.secret_code), Game.NUM_SECRET_PEGS)


class BaseViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        """
        Create a game
        """
        Game.objects.create()
