import random, re
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Game, get_random_color, Guess
from .serializers import GameSerializer, GuessSerializer
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
        when a POST request is made to the mastermind/start
        """
        # check api response
        expected_data = GameSerializer(self.expected_obj)
        self.assertEqual(self.response.data, expected_data.data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_create_secret_code(self):
        """
        Ensures that a game is created with a secret_code
        when a POST request is made to the mastermind/start
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

    def get_wrong_code(self):
        code = []
        while not code or code == self.game.secret_code:  # create a code different than secret code
            code = self.generate_code_guess(Game.NUM_SECRET_PEGS,
                                            get_random_color)
        return code


class GuessCode(BaseViewTest):
    # POST url
    URL = reverse("guess")
    # required game id error
    REQUIRED_GAME = {'game': [ErrorDetail(string='This field may not be null.', code='null')]}
    # invalid code guess error
    INVALID_CODE = {'code_guess': [
        ErrorDetail(string='Guess code is invalid. It must be an string color list of ' + str(
            Game.NUM_SECRET_PEGS) + ' length.', code='invalid')]}

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
        when a POST request without params is made to the mastermind/guess
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
        when a POST request with invalid game_id is made to the mastermind/guess
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
        when a POST request without code_guess is made to the mastermind/guess
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
        when a POST request with invalid code guess length is made to the mastermind/guess
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
        when a POST request with invalid values in code guess is made to the mastermind/guess
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
        when a POST request with valid params is made to the mastermind/guess
        """
        expected_data = r"[0-" + str(Game.NUM_SECRET_PEGS) + "] black(s?), [0-" + str(
            Game.NUM_SECRET_PEGS) + "] white(s?)"
        # API endpoint
        code = self.get_wrong_code()
        params = {'game_id': self.game.pk, 'code_guess': code}
        response = self.client.post(self.URL, params)

        # check api response
        self.assertTrue(re.match(expected_data, response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_valid(self):
        """
        Ensures that API status response is 200 (OK)
        and data response are how many whites and black pegs should have the decoding board
        when a POST request with valid params is made to the mastermind/guess
        """
        expected_data = "2 blacks, 2 whites"

        # almost secret code as code guess
        self.game.secret_code = ["RED", "BLUE", "GREEN", "RED"]
        self.game.save()
        code = ["RED", "BLUE", "RED", "GREEN"]

        # API endpoint
        params = {'game_id': self.game.pk, 'code_guess': code}
        response = self.client.post(self.URL, params)

        # check api response
        self.assertEqual(expected_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_guess(self):
        """
        Ensures that a guess is created
        when a POST request with valid params is made to the mastermind/guess
        """
        expected_data = len(Guess.objects.all()) + 1
        # API endpoint
        code = self.generate_code_guess(Game.NUM_SECRET_PEGS,
                                        get_random_color)
        params = {'game_id': self.game.pk, 'code_guess': code}
        self.client.post(self.URL, params)

        # check api response
        self.assertTrue(expected_data, len(Guess.objects.all()))

    def test_user_wins(self):
        """
        Ensures that API status response is 200 (OK)
        and data response is winning message
        when a POST request with secret code as guess code is made to the mastermind/guess
        """
        expected_data = Game.WINNIG_MSG
        # API endpoint
        params = {'game_id': self.game.pk, 'code_guess': self.game.secret_code}
        response = self.client.post(self.URL, params)

        # check api response
        self.assertTrue(expected_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_already_won(self):
        """
        Ensures that API status response is 200 (OK)
        and data response is already won message
        when a POST request with secret code as guess code is made to the mastermind/guess
        """
        expected_data = Game.ALREADY_WON_MSG
        # API endpoint
        for times in range(2):
            params = {'game_id': self.game.pk, 'code_guess': self.game.secret_code}
            response = self.client.post(self.URL, params)

        # check api response
        self.assertTrue(expected_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_game_over(self):
        """
        Ensures that API status response is 200 (OK)
        and data response is game over message due to more than 11 guesses in this game
        when a POST request is made to the mastermind/guess
        """
        expected_data = Game.GAME_OVER_MSG
        # API endpoint
        for idx in range(Game.MAX_GUESSES):
            code = self.get_wrong_code()
            params = {'game_id': self.game.pk, 'code_guess': code}
            response = self.client.post(self.URL, params)

        # check api response
        self.assertTrue(expected_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_new_guess_after_winning(self):
        """
        Ensures that API status response is 200 (OK)
        and data response is winning message even after giving a new guess
        when a POST request with secret code as guess code is made to the mastermind/guess
        """
        expected_data = Game.WINNIG_MSG
        # API endpoint
        params = {'game_id': self.game.pk, 'code_guess': self.get_wrong_code()}
        response = self.client.post(self.URL, params)

        # check api response
        self.assertTrue(expected_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllGameGuesses(BaseViewTest):

    def create_guess(self):
        Guess.objects.create(game=self.game, code_guess=self.get_wrong_code())

    def setUp(self):
        super().setUp()
        for idx in range(5):
            self.create_guess()  # creates guesses for a game

    def test_get_all_game_guesses(self):
        """
        Ensures that API status response is 200 (OK)
        and data response is all guesses of a game
        when a POST request is made to the mastermind/historic
        """
        # API endpoint
        response = self.client.get(reverse("historic", kwargs={"game": self.game.pk}))
        # fetch the data from db
        expected = Guess.objects.filter(game=self.game)
        serialized = GuessSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_game_guesses_invalid_game_id(self):
        """
        Ensures that API status response is 404 (Not found)
        when a POST request with invalid game id is made to the mastermind/historic
        """
        expected_data = {'detail': ErrorDetail(string='Not found.', code='not_found')}
        # API endpoint
        response = self.client.get(reverse("historic", kwargs={"game": self.game.pk + 1}))
        # fetch the data from db
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
