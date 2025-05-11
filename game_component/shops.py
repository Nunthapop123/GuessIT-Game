import pygame as pg
import sys
from game_component.constants import SCREEN, WIDTH, HEIGHT, BOMB_ICON, MAGNIFY_ICON


class Shop:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.items_available = {"Bomb": 30, "Magnify": 20}

    def display_item(self):
        SCREEN.fill("white")

        title_font = pg.font.Font("assets/PressStart2P-vaV7.ttf", 65)
        item_font = pg.font.Font("assets/PressStart2P-vaV7.ttf", 20)

        title = title_font.render("SHOP", True, "black")
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        SCREEN.blit(title, title_rect)

        player_score = self.game_manager.player.score
        score_text = item_font.render(f"Your Points: {player_score}", True, "black")
        score_rect = score_text.get_rect(center=(WIDTH // 2, 160))
        SCREEN.blit(score_text, score_rect)

        player_level = self.game_manager.player.level
        level_text = item_font.render(f"Next Level: {player_level}", True, "black")
        level_rect = level_text.get_rect(center=(1100, 40))
        SCREEN.blit(level_text, level_rect)

        self.buttons = {}
        item_names = list(self.items_available.keys())
        start_x = 200
        gap_x = 300
        y_pos = 300

        for i, item_name in enumerate(item_names):
            cost = self.items_available[item_name]

            item_text = item_font.render(f"{item_name} - {cost} pts", True, "black")
            item_text_rect = item_text.get_rect(center=(start_x + i * gap_x, y_pos + 50))
            SCREEN.blit(item_text, item_text_rect)
            if item_name == "Bomb":
                SCREEN.blit(BOMB_ICON, (item_text_rect.centerx - 55, y_pos - 60))
            elif item_name == "Magnify":
                SCREEN.blit(MAGNIFY_ICON, (item_text_rect.centerx - 35, y_pos - 60))
            buy_button = pg.Rect(start_x + i * gap_x - 75, y_pos + 70, 150, 40)
            pg.draw.rect(SCREEN, (0, 150, 0), buy_button, border_radius=10)
            button_text = item_font.render("Buy", True, "white")
            button_rect = button_text.get_rect(center=buy_button.center)
            SCREEN.blit(button_text, button_rect)

            self.buttons[item_name] = buy_button

        font_button = pg.font.Font("assets/PressStart2P-vaV7.ttf", 20)
        continue_text = font_button.render("Continue", True, "white")
        self.continue_button = pg.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 40)
        pg.draw.rect(SCREEN, (0, 0, 200), self.continue_button, border_radius=10)
        continue_text_rect = continue_text.get_rect(center=self.continue_button.center)
        SCREEN.blit(continue_text, continue_text_rect)
        pg.display.update()

    def confirm_purchase(self, item_name):
        previous_screen = SCREEN.copy()

        overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        SCREEN.blit(previous_screen, (0, 0))
        SCREEN.blit(overlay, (0, 0))

        popup_rect = pg.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 100, 500, 200)
        pg.draw.rect(SCREEN, "white", popup_rect, border_radius=15)
        pg.draw.rect(SCREEN, "black", popup_rect, 4, border_radius=15)

        title_font = pg.font.Font("assets/PressStart2P-vaV7.ttf", 24)
        text_font = pg.font.Font("assets/PressStart2P-vaV7.ttf", 18)

        msg = title_font.render(f"Buy {item_name}?", True, "black")
        msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        SCREEN.blit(msg, msg_rect)

        cost = self.items_available[item_name]
        cost_text = text_font.render(f"This will cost {cost} pts", True, "black")
        cost_rect = cost_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        SCREEN.blit(cost_text, cost_rect)

        yes_button = pg.Rect(WIDTH // 2 - 140, HEIGHT // 2 + 40, 100, 40)
        no_button = pg.Rect(WIDTH // 2 + 40, HEIGHT // 2 + 40, 100, 40)

        pg.draw.rect(SCREEN, (0, 150, 0), yes_button, border_radius=8)
        pg.draw.rect(SCREEN, (200, 0, 0), no_button, border_radius=8)

        yes_text = text_font.render("Yes", True, "white")
        no_text = text_font.render("No", True, "white")
        SCREEN.blit(yes_text, yes_text.get_rect(center=yes_button.center))
        SCREEN.blit(no_text, no_text.get_rect(center=no_button.center))
        pg.display.update()

        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if yes_button.collidepoint(event.pos):
                        self.purchase_item(item_name)
                        waiting = False
                    elif no_button.collidepoint(event.pos):
                        self.display_item()
                        waiting = False
            pg.time.delay(10)

    def purchase_item(self, item_name):
        player = self.game_manager.player
        cost = self.items_available[item_name]

        if player.score >= cost:
            player.score -= cost
            player.items[item_name] += 1
            print(f"{item_name} purchased! Remaining score: {player.score}")
        else:
            print("Not enough points!")

        self.display_item()