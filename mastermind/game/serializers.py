from rest_framework import serializers
from .models import Game, Guess


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["pk"]


class GuessSerializer(serializers.ModelSerializer):
    ERR_MSG_INVALID_CODE = "Guess code is invalid. It must be an string color list of " \
                           + str(Game.NUM_SECRET_PEGS) + " length."

    code_guess = serializers.ListField(child=serializers.CharField(), required=True)

    def validate_code_guess(self, value):
        """Check if list length and list values are correct"""
        if len(value) != Game.NUM_SECRET_PEGS or not all(n in [color[0] for color in Game.COLORS] for n in value):
            raise serializers.ValidationError(self.ERR_MSG_INVALID_CODE)
        return value

    class Meta:
        model = Guess
        fields = "__all__"
