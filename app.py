import pygame as pg
import sys
import random

pg.init()

WIDTH = 1280
HEIGHT = 1024
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pg.image.load("assets/Starting Tiles(white).png")
BACKGROUND_RECT = BACKGROUND.get_rect(center=(640, 450))
LETTER_FONT = pg.font.Font("assets/PressStart2P-vaV7.ttf", 40)

OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"

HEADER = LETTER_FONT.render('GuessIT!', True, 'black')
HEADER_RECT = HEADER.get_rect()
HEADER_RECT.center = ((1280 // 2, 100))

SCREEN.fill("white")
SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
SCREEN.blit(HEADER, HEADER_RECT)
pg.display.update()

LETTER_X_SPACING = 85
LETTER_Y_SPACING = 162
LETTER_SIZE = 75

guesses_count = 0
guesses = [[]] * 6

current_guess = []
current_guess_letter = ""
current_letter_bg_x = 432


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


def create_new_letter():
    global current_guess_letter, current_letter_bg_x
    current_guess_letter += key_pressed
    new_letter = Letter(key_pressed, (current_letter_bg_x, guesses_count * 100 + LETTER_Y_SPACING))
    current_letter_bg_x += LETTER_X_SPACING
    guesses[guesses_count].append(new_letter)
    current_guess.append(new_letter)
    for guess in guesses:
        for letter in guess:
            letter.draw()


def delete_letter():
    global current_guess_letter, current_letter_bg_x
    guesses[guesses_count][-1].delete()
    guesses[guesses_count].pop()
    current_guess_letter = current_guess_letter[:-1]
    current_guess.pop()
    current_letter_bg_x -= LETTER_X_SPACING


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            key_pressed = event.unicode.upper()
            if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                if len(current_guess_letter) < 5:
                    create_new_letter()
            if event.key == pg.K_BACKSPACE:
                if len(current_guess_letter) > 0:
                    delete_letter()


class Word:
    pass


class Player:
    pass


class Item:
    pass


class Shop:
    pass


class GameManager:
    pass
