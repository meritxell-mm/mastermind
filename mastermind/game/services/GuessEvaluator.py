class GuessEvaluator:
    @staticmethod
    def evaluate_guess(guess):
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
        return guess