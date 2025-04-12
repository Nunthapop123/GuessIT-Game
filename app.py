import pygame as pg
import sys
import random
from words import *

pg.init()

WIDTH = 1280
HEIGHT = 1024
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pg.image.load("assets/Starting Tiles(white).png")
BACKGROUND_RECT = BACKGROUND.get_rect(center=(640, 450))

OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"
GREEN = "#D3E671"
YELLOW = "#F8ED8C"

LETTER_FONT = pg.font.Font("assets/PressStart2P-vaV7.ttf", 40)
LETTER_X_SPACING = 85
LETTER_Y_SPACING = 162
LETTER_SIZE = 75


class Letter:
    def __init__(self, text, bg_position):
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (bg_position[0], self.bg_y, LETTER_SIZE, LETTER_SIZE)
        self.text = text
        self.text_position = (self.bg_x + 36, self.bg_position[1] + 34)
        self.text_surface = LETTER_FONT.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

    def draw(self):
        pg.draw.rect(SCREEN, self.bg_color, self.bg_rect)
        if self.bg_color == "white":
            pg.draw.rect(SCREEN, FILLED_OUTLINE, self.bg_rect, 3)
        self.text_surface = LETTER_FONT.render(self.text, True, self.text_color)
        SCREEN.blit(self.text_surface, self.text_rect)
        pg.display.update()

    def delete(self):
        pg.draw.rect(SCREEN, "white", self.bg_rect)
        pg.draw.rect(SCREEN, OUTLINE, self.bg_rect, 3)
        pg.display.update()


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


class Player:
    pass


class Item:
    pass


class Shop:
    pass


class GameManager:
    def __init__(self):
        self.word = Word()
        self.game_result = ""
        self.guesses = [[]] * 6
        self.current_guess = []
        self.current_guess_letter = ""
        self.current_letter_bg_x = 432
        self.guesses_count = 0
        self.running = True
        self.starter_display()

    def starter_display(self):
        SCREEN.fill("white")
        SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
        header = LETTER_FONT.render("GuessIT!", True, "black")
        header_rect = header.get_rect(center=(WIDTH // 2, 100))
        SCREEN.blit(header, header_rect)
        pg.display.update()

    def create_new_letter(self, key_pressed):
        self.current_guess_letter += key_pressed
        new_letter = Letter(key_pressed, (self.current_letter_bg_x, self.guesses_count * 100 + LETTER_Y_SPACING))
        self.current_letter_bg_x += LETTER_X_SPACING
        self.guesses[self.guesses_count].append(new_letter)
        self.current_guess.append(new_letter)
        for guess in self.guesses:
            for letter in guess:
                letter.draw()

    def delete_letter(self):
        self.current_guess[-1].delete()
        self.guesses[self.guesses_count].pop()
        self.current_guess.pop()
        self.current_guess_letter = self.current_guess_letter[:-1]
        self.current_letter_bg_x -= LETTER_X_SPACING

    def handle_guesses(self):
        guess_str = ''.join([letter.text for letter in self.current_guess]).lower()
        if guess_str in WORDS:
            result = self.word.check_guess(self.current_guess)
            self.game_result = result
            self.guesses_count += 1
            self.current_guess = []
            self.current_guess_letter = ""
            self.current_letter_bg_x = 432
            if result == "W":
                print("You Win!")
            elif self.guesses_count == 6 and result == "":
                self.game_result = "L"
                print(f"You Lose! The word was: {self.word.correct_word.upper()}")
        else:
            print(f"'{guess_str.upper()}' is not a valid word!")

    def play_again(self):
        pg.draw.rect(SCREEN, "white", (10, 800, 1000, 800))
        play_again_font = LETTER_FONT
        play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "black")
        play_again_rect = play_again_text.get_rect(center=(WIDTH / 2, 900))
        corrected_word_text = play_again_font.render(f"The word was {self.word.correct_word}!", True, "black")
        corrected_word_rect = corrected_word_text.get_rect(center=(WIDTH / 2, 850))
        SCREEN.blit(corrected_word_text, corrected_word_rect)
        SCREEN.blit(play_again_text, play_again_rect)
        pg.display.update()

    def reset(self):
        SCREEN.fill("white")
        SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
        self.game_result = ""
        self.guesses = [[]] * 6
        self.current_guess = []
        self.current_guess_letter = ""
        self.guesses_count = 0
        self.word = Word()
        pg.display.update()

    def game_loop(self):
        while self.running:
            if self.game_result != "":
                self.play_again()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        if len(self.current_guess_letter) > 0:
                            self.delete_letter()
                    elif event.key == pg.K_RETURN:
                        if self.game_result != "":
                            self.reset()
                        else:
                            if len(self.current_guess_letter) == 5:
                                self.handle_guesses()
                    else:
                        key_pressed = event.unicode.upper()
                        if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                            if len(self.current_guess_letter) < 5:
                                self.create_new_letter(key_pressed)


if __name__ == '__main__':
    game = GameManager()
    game.game_loop()
