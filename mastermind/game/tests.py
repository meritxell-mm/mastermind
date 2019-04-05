from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Game, NUM_SECRET_PEGS
from .serializers import GameSerializer


# Create your tests here.
class BaseViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        Game.objects.create()


class CreateGame(BaseViewTest):

    def test_create_game(self):
        """
        This test ensures that a game with a secret code is created
        when a GET request is made to the game/api/new
        """
        # API endpoint
        response = self.client.get(
            reverse("new_game")
        )
        # fetch db data
        expected_obj = Game.objects.all()
        # check object values
        self.assertTrue(expected_obj)
        self.assertEqual(len(expected_obj.secret_code), NUM_SECRET_PEGS)
        # check api response
        expected_data = GameSerializer(expected_obj)
        self.assertEqual(response.data, expected_data.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



