from django.shortcuts import render
from .models import Game
from .serializers import GameSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class NewGame(APIView):
    def post(self, request):
        """
        Creates new game with secret code
        :return: game id
        """
        game = Game.objects.create()
        serializer = GameSerializer(game)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
