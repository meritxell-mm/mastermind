from rest_framework import serializers
from .models import Game, Guess


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["pk"]


class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = ['id', 'game', 'code_guess', 'black_pegs', 'white_pegs', 'create_date']

    def plural_pegs(self, count):
        """
        Get plural char 's' if needed
        :param count: number of pegs
        :return: string 's' or empty string
        """
        return 's' if count > 1 else ''

    @property
    def result_message(self):
        """
        Get string response given a guess code
        :param black_pegs: number of black pegs
        :param white_pegs: number of white pegs
        :return: string
        """
        black_plural = self.plural_pegs(self.instance.black_pegs)
        white_plural = self.plural_pegs(self.instance.white_pegs)
        return f"{self.instance.black_pegs} black peg{black_plural}, {self.instance.white_pegs} white peg{white_plural}"