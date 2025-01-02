import random
from django.db import models
from django.contrib.postgres.fields import ArrayField


def get_random_color():
    """
    Get random color from color choices
    :return: string color
    """
    return Game.COLORS[random.randint(0, len(Game.COLORS) - 1)][0]


def create_secret_code():
    """
    Creates a secret code based on random pegs
    :return: list of random colors
    """
    secret_code = []

    for idx in range(Game.NUM_SECRET_PEGS):
        secret_code.append(get_random_color())

    return secret_code


class Game(models.Model):
    # Already won message
    ALREADY_WON_MSG = "Game already won"

    # Winning message
    WINNIG_MSG = "Congratulations! YOU WON!!!"

    # Game over message
    GAME_OVER_MSG = "GAME OVER"

    # Game not found message
    ERR_MSG_INVALID_GAME = "Invalid game id. Game not found."

    # number of pegs to guess
    NUM_SECRET_PEGS = 4

    # number of guesses allowed
    MAX_GUESSES = 11

    # define colors choices
    COLORS = (
        ('WHITE', 'WHITE'),
        ('YELLOW', 'YELLOW'),
        ('ORANGE', 'ORANGE'),
        ('RED', 'RED'),
        ('GREEN', 'GREEN'),
        ('BLUE', 'BLUE'),
        ('BROWN', 'BROWN'),
        ('BLACK', 'BLACK'),
    )

    is_won = models.BooleanField(default=False)
    secret_code = ArrayField(models.CharField(choices=COLORS, max_length=10),
                             size=NUM_SECRET_PEGS,
                             default=create_secret_code,
                             editable=False)


class Guess(models.Model):
    ERR_MSG_INVALID_CODE = "Guess code is invalid. It must be an string color list of " + str(
        Game.NUM_SECRET_PEGS) + " length."
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='guesses')
    create_date = models.DateTimeField(auto_now_add=True)
    code_guess = ArrayField(models.CharField(choices=Game.COLORS, max_length=10),
                            size=Game.NUM_SECRET_PEGS,
                            editable=False)
    black_pegs = models.IntegerField(default=0)
    white_pegs = models.IntegerField(default=0)

    class Meta:
        ordering = ['game', 'create_date']
