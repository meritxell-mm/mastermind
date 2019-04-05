import random
from django.db import models
from django.contrib.postgres.fields import ArrayField


def create_secret_code():
    """
    Creates a random secret code of pegs
    :return: A secret code pegs list
    """
    secret_code = []

    for idx in range(Game.NUM_SECRET_PEGS):
        secret_code.append(random.randint(0, len(Game.COLORS) - 1))

    return secret_code


class Game(models.Model):
    # number of pegs to guess
    NUM_SECRET_PEGS = 4

    # number of guesses allowed
    MAX_GUESSES = 11

    # define colors
    WHITE = 0
    YELLOW = 1
    ORANGE = 2
    RED = 3
    GREEN = 4
    BLUE = 5
    BROWN = 6
    BLACK = 7

    # define colors choices
    COLORS = (
        (WHITE, 'WHITE'),
        (YELLOW, 'YELLOW'),
        (ORANGE, 'ORANGE'),
        (RED, 'RED'),
        (GREEN, 'GREEN'),
        (BLUE, 'BLUE'),
        (BROWN, 'BROWN'),
        (BLACK, 'BLACK'),
    )

    secret_code = ArrayField(models.IntegerField(choices=COLORS),
                             size=NUM_SECRET_PEGS,
                             default=create_secret_code,
                             editable=False)


class Guess(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    code_guess = ArrayField(ArrayField(models.IntegerField(choices=Game.COLORS),
                                       size=Game.NUM_SECRET_PEGS,
                                       editable=False))
    correct_positions = models.IntegerField(default=0)
    correct_colors = models.IntegerField(default=0)

    class Meta:
        ordering = ['game', 'create_date']
