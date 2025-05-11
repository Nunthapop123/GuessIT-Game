import random
from game_component.constants import GREEN, YELLOW
from game_component.words_data import WORDS

class Word:
    def __init__(self):
        self.correct_word = self.generate_new_word()

    def check_guess(self, guess_word):
        correct = list(self.correct_word)
        game_decided = False
        game_result = ""

        for i in range(5):
            letter_obj = guess_word[i]
            lowercase_letter = letter_obj.text.lower()

            if lowercase_letter == correct[i]:
                letter_obj.bg_color = GREEN
                letter_obj.text_color = "white"
                if not game_decided:
                    game_result = "W"
            elif lowercase_letter in correct:
                letter_obj.bg_color = YELLOW
                letter_obj.text_color = "white"
                game_result = ""
                game_decided = True
            else:
                letter_obj.bg_color = "grey"
                letter_obj.text_color = "white"
                game_result = ""
                game_decided = True

            letter_obj.draw()

        return game_result

    def generate_new_word(self):
        return random.choice(WORDS)