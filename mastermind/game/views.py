from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Game
from .serializers import GameSerializer, GuessSerializer
from .models import Guess
from .services.GuessEvaluator import GuessEvaluator


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
        Given a code guess, and game id returns guess response.
        :return: string representing the number of white and black pegs. Ex:'1 black, 2 whites'
                or string Game.GAME_OVER_MSG if Game.MAX_GUESSES is exceeded
                or string Game.WINNING_MSG in case the code was broken
                or string Game.ALREADY_WON_MSG in case the code was already won
        """
        game_id = request.POST.get('game_id', None)
        code_guess = request.POST.getlist('code_guess', [])

        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            return Response(Game.ERR_MSG_INVALID_GAME, status=status.HTTP_404_NOT_FOUND)

        if game.is_won:
            return Response(Game.ALREADY_WON_MSG, status.HTTP_200_OK)
        elif game.guesses.count() > game.MAX_GUESSES:
            return Response(Game.GAME_OVER_MSG, status.HTTP_200_OK)

        guess = Guess.objects.create(game=game, code_guess=code_guess)
        GuessEvaluator.evaluate_guess(guess)

        if guess.black_pegs == Game.NUM_SECRET_PEGS:
            game.is_won = True
            game.save()
            return Response(Game.WINNIG_MSG, status.HTTP_200_OK)

        guess_serializer = GuessSerializer(guess)

        return Response({
            guess_serializer.result_message,
        }, status.HTTP_200_OK)


class GuessList(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = GuessSerializer

    def get_queryset(self, *args, **kwargs):
        return Guess.objects.filter(game=get_object_or_404(Game, pk=self.kwargs['game']))
