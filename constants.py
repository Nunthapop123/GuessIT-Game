import pygame as pg

pg.init()

WIDTH = 1280
HEIGHT = 1024
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pg.image.load("assets/Starting Tiles(white).png")
BACKGROUND_RECT = BACKGROUND.get_rect(center=(WIDTH // 2, 450))

OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"
GREEN = "#D3E671"
YELLOW = "#F8ED8C"

LETTER_FONT = pg.font.Font("assets/PressStart2P-vaV7.ttf", 40)
BOMB_ICON = pg.image.load("assets/bomb_icon.png")
MAGNIFY_ICON = pg.image.load("assets/magnify_icon.png")
BOMB_ICON = pg.transform.scale(BOMB_ICON, (105, 105))
MAGNIFY_ICON = pg.transform.scale(MAGNIFY_ICON, (105, 105))

LETTER_X_SPACING = 85
LETTER_Y_SPACING = 162
LETTER_SIZE = 75
