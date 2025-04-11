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

HEADER = LETTER_FONT.render('GuessIT!', True, 'black')
HEADER_RECT = HEADER.get_rect()
HEADER_RECT.center = ((1280 // 2, 100))

SCREEN.fill("white")
SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
SCREEN.blit(HEADER, HEADER_RECT)
pg.display.update()


class Letter:
    pass


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


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
