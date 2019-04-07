from .models import Game, Guess
from .serializers import GameSerializer, GuessSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.shortcuts import get_object_or_404


class NewGame(APIView):
    def post(self, request):
        """
        Creates new game with secret code
        :return: dict game pk
        """
        game = Game.objects.create()
        serializer = GameSerializer(game)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GuessCode(APIView):
    def post(self, request):
        """
        Given a code guess, and game id returns guess respose.
        :return: string representing the number of white and black pegs. Ex:'1 black, 2 whites'
                or string Game.GAME_OVER_MSG if Game.MAX_GUESSES is exceeded
                or string Game.WINNING_MSG in case the code was broken
                or string Game.ALREADY_WON_MSG in case the code was already won
        """
        game_id = request.POST.get('game_id', None)
        code_guess = request.POST.getlist('code_guess', [])

        serializer = GuessSerializer(data={'game': game_id, 'code_guess': code_guess})
        if serializer.is_valid(raise_exception=True):
            return Response(self.give_game_result(game_id, serializer), status.HTTP_200_OK)

    def give_game_result(self, game_id, serializer):
        """
        Given a code guess, calculates how many pegs are correct in both color and position,
        represented by black pegs, and how many pegs have correct color (but wrong position),
        represented by white pegs and returns an appropriate answer.
        :param game_id: int game id of current guess
        :param serializer: GuessSerializer of current guess

        :return: string representing the number of white and black pegs. Ex:'1 black, 2 whites'
                or string "GAME OVER" if MAX_GUESSES is exceeded
                or string "YOU WON!!" in case the code was broken
        """
        if Guess.objects.filter(game=game_id, black_pegs=4).exists():
            return Game.ALREADY_WON_MSG
        elif Guess.objects.filter(game=game_id).count() > Game.MAX_GUESSES:
            return Game.GAME_OVER_MSG
        else:
            guess = serializer.save()
            black_pegs, white_pegs = self.get_correct_pegs(guess)
            if black_pegs == Game.NUM_SECRET_PEGS:
                return Game.WINNIG_MSG
            return self.get_guess_response(black_pegs, white_pegs)

    @staticmethod
    def get_correct_pegs(guess):
        """
        Get number black and white pegs
        :param guess: Guess instance of current guess
        :return: int black_pegs, int white_pegs
        """
        secret_code = guess.game.secret_code
        code_guess = guess.code_guess
        code_guess_aux = code_guess.copy()
        secret_code_aux = secret_code.copy()
        black_pegs = 0
        white_pegs = 0

        # find black pegs first
        for idx, color in enumerate(code_guess):
            if secret_code[idx] == color:
                black_pegs += 1
                code_guess_aux[idx] = None
                secret_code_aux[idx] = None

        # find white pegs
        for idx, color in enumerate(code_guess_aux):
            if color and color in secret_code_aux:
                white_pegs += 1
                secret_code_aux[secret_code_aux.index(color)] = None

        guess.black_pegs = black_pegs
        guess.white_pegs = white_pegs
        guess.save()
        return black_pegs, white_pegs

    @staticmethod
    def plural_pegs(small_pegs):
        """
        Get plural char 's' if needed
        :param small_pegs: number of pegs
        :return: string 's' or empty string
        """
        return 's' if small_pegs > 1 else ''

    def get_guess_response(self, black_pegs, white_pegs):
        """
        Get string response given a guess code
        :param black_pegs: number of black pegs
        :param white_pegs: number of white pegs
        :return: string
        """
        return "{0} black{1}, {2} white{3}".format(black_pegs, self.plural_pegs(black_pegs),
                                                   white_pegs, self.plural_pegs(white_pegs))


class GuessList(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = GuessSerializer

    def get_queryset(self, *args, **kwargs):
        return Guess.objects.filter(game=get_object_or_404(Game, pk=self.kwargs['game']))
