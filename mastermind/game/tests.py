import random, re
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Game, get_random_color
from .serializers import GameSerializer
from rest_framework.exceptions import ErrorDetail


class CreateGame(APITestCase):
    response = None
    expected_obj = None

    def setUp(self):
        # API endpoint
        self.response = self.client.post(
            reverse("new_game")
        )
        # fetch db data
        self.expected_obj = Game.objects.all()[0]

    def test_create_game(self):
        """
        Ensures that api response is the game id
        when a POST request is made to the mastermind/api/new
        """
        # check api response
        expected_data = GameSerializer(self.expected_obj)
        self.assertEqual(self.response.data, expected_data.data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_create_secret_code(self):
        """
        Ensures that a game is created with a secret_code
        when a POST request is made to the mastermind/api/new
        """
        # check object values
        self.assertTrue(self.expected_obj)
        self.assertEqual(len(self.expected_obj.secret_code), Game.NUM_SECRET_PEGS)


class BaseViewTest(APITestCase):
    client = APIClient()
    game = None

    def setUp(self):
        """
        Create a game
        """
        self.game = Game.objects.create()


class GuessCode(BaseViewTest):
    # POST url
    URL = reverse("guess_code")
    # required game id error
    REQUIRED_GAME = {'game': [ErrorDetail(string='This field may not be null.', code='null')]}
    # invalid code guess error
    INVALID_CODE = {'code_guess': [
        ErrorDetail(string='Guess code is invalid. It must be an string color list of ' + str(
            Game.NUM_SECRET_PEGS) + ' length.', code='invalid')]}

    @staticmethod
    def generate_code_guess(length, value):
        """
        Create a code guess with specific length and values
        :param length: length of code guess list
        :param value: function or variable to get a value for a code guess position in list
        :return: code guess
        """
        code = []
        is_callable = callable(value)
        for idx in range(length):
            if is_callable:
                code.append(value())
            else:
                code.append(value)
        return code

    def get_invalid_game_error(self):
        """
        Get invalid game id error (using latest pk which is the recent created game for the test plus 1)
        :return error dict
        """
        return {'game': [
            ErrorDetail(string='Invalid pk "' + str(self.game.pk + 1) + '" - object does not exist.',
                        code='does_not_exist')]}

    def test_request_without_params(self):
        """
        Ensures that API response is 400 (Bad request)
        when a POST request without params is made to the mastermind/api/guess_code
        """
        expected_response = {**self.REQUIRED_GAME, **self.INVALID_CODE}

        # API endpoint
        params = {}
        response = self.client.post(self.URL, params)

        # check api response
        self.assertEqual(response.data, expected_response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_with_invalid_game_id(self):
        """
        Ensures that API response is 400 (Bad Request)
        when a POST request with invalid game_id is made to the mastermind/api/guess_code
        """
        expected_response = self.get_invalid_game_error()

        # API endpoint
        code = GuessCode.generate_code_guess(Game.NUM_SECRET_PEGS,
                                             get_random_color)
        params = {'game_id': self.game.pk + 1, 'code_guess': code}
        response = self.client.post(self.URL, params)

        # check api response
        self.assertEqual(response.data, expected_response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_without_code_guess(self):
        """
        Ensures that API response is 400 (Bad request)
        when a POST request without code_guess is made to the mastermind/api/guess_code
        """
        expected_response = self.INVALID_CODE

        # API endpoint
        params = {'game_id': self.game.pk}
        response = self.client.post(self.URL, params)

        # check api response
        self.assertEqual(response.data, expected_response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_with_invalid_code_length(self):
        """
        Ensures that API response is 400 (Bad request)
        when a POST request with invalid code guess length is made to the mastermind/api/guess_code
        """
        # create invalid code with Game.NUM_SECRET_PEGS+1 length
        code = GuessCode.generate_code_guess(Game.NUM_SECRET_PEGS + 1,
                                             get_random_color)
        # API endpoint
        params = {'game_id': self.game.pk, 'code_guess': code}
        response = self.client.post(self.URL, params)

        # check api response
        self.assertEqual(response.data, self.INVALID_CODE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_with_invalid_code_guess_values(self):
        """
        Ensures that API response is 400 (Bad request)
        when a POST request with invalid values in code guess is made to the mastermind/api/guess_code
        """
        # API endpoint
        code = self.generate_code_guess(Game.NUM_SECRET_PEGS, 'test')  # creates 'test' array
        params = {'game_id': self.game.pk, 'code_guess': code}
        response = self.client.post(self.URL, params)

        # check api response
        self.assertEqual(response.data, self.INVALID_CODE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_valid(self):
        """
        Ensures that API status response is 200 (OK)
        and data response are how many whites and black pegs should have the decoding board
        when a POST request with valid params is made to the mastermind/api/guess_code
        """
        expected_data = r"[0-" + str(Game.NUM_SECRET_PEGS) + "] black(s?), [0-" + str(
            Game.NUM_SECRET_PEGS) + "] white(s?)"
        # API endpoint
        code = self.generate_code_guess(Game.NUM_SECRET_PEGS,
                                        get_random_color)
        params = {'game_id': self.game.pk, 'code_guess': code}
        response = self.client.post(self.URL, params)

        # check api response
        self.assertTrue(re.match(expected_data, response.data))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
