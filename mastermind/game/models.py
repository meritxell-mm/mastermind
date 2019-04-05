from django.db import models


class Peg(models.Model):
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

    position = models.IntegerField()
    color = models.IntegerField(choices=COLORS)


class Guess(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    code_guess = models.ManyToManyField(Peg)
    correct_positions = models.IntegerField(default=0)
    correct_colors = models.IntegerField(default=0)


class Game(models.Model):
    secret_code = models.ManyToManyField(Peg)
    guesses = models.ManyToManyField(Guess)
