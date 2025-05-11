import pygame as pg
import sys
import random
from constants import SCREEN, WIDTH, HEIGHT, BOMB_ICON, MAGNIFY_ICON, LETTER_FONT, LETTER_X_SPACING, LETTER_Y_SPACING, \
    BACKGROUND, BACKGROUND_RECT
from words import Word
from words_data import WORDS
from player import Player
from letters import Letter
from items import Bomb, Magnifying_Glass
from stats import GameStats
from shops import Shop
import subprocess


class GameManager:
    def __init__(self):
        self.word = Word()
        self.player = Player()
        self.game_result = ""
        self.game_state = "menu"
        self.guesses = [[] for i in range(6)]
        self.current_guess = []
        self.current_guess_letter = ""
        self.current_letter_bg_x = 432
        self.player.attempts = 0
        self.shop = None
        self.game_over_displayed = False
        self.running = True
        self.level_logs = []
        self.menu_display()

    def menu_display(self):
        SCREEN.fill("white")

        title_font = pg.font.Font("assets/PressStart2P-vaV7.ttf", 65)
        title = title_font.render("GuessIT!", True, "black")
        title_rect = title.get_rect(center=(WIDTH // 2, 200))

        play_text = LETTER_FONT.render("Play", True, "white")
        self.play_button_rect = pg.Rect(WIDTH // 2 - 150, 460, 300, 70)
        pg.draw.rect(SCREEN, (20, 200, 0), self.play_button_rect, border_radius=10)
        play_text_rect = play_text.get_rect(center=self.play_button_rect.center)

        stat_text = LETTER_FONT.render("Stats", True, "white")
        self.stat_button_rect = pg.Rect(WIDTH // 2 - 150, 560, 300, 70)
        pg.draw.rect(SCREEN, (200, 150, 20), self.stat_button_rect, border_radius=10)
        stat_text_rect = stat_text.get_rect(center=self.stat_button_rect.center)

        exit_text = LETTER_FONT.render("Exit", True, "white")
        self.exit_button_rect = pg.Rect(WIDTH // 2 - 150, 660, 300, 70)
        pg.draw.rect(SCREEN, (200, 0, 0), self.exit_button_rect, border_radius=10)
        exit_text_rect = exit_text.get_rect(center=self.exit_button_rect.center)

        SCREEN.blit(title, title_rect)
        SCREEN.blit(play_text, play_text_rect)
        SCREEN.blit(exit_text, exit_text_rect)
        SCREEN.blit(stat_text, stat_text_rect)

        pg.display.update()

    def starter_display(self):
        SCREEN.fill("white")
        SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
        header = LETTER_FONT.render("GuessIT!", True, "black")
        header_rect = header.get_rect(center=(WIDTH // 2, 100))

        player_feature_font = pg.font.Font("assets/PressStart2P-vaV7.ttf", 20)

        level_text = player_feature_font.render(f"Level: {self.player.level}", True, "black")
        level_text_rect = level_text.get_rect(center=(1100, 50))

        score_text = player_feature_font.render(f"Score: {self.player.score}", True, "black")
        score_text_rect = score_text.get_rect(center=(150, 50))

        menu_text = player_feature_font.render("<< Menu", True, "white")
        self.menu_button_rect = pg.Rect(50, 950, 150, 40)
        pg.draw.rect(SCREEN, (200, 0, 0), self.menu_button_rect, border_radius=10)
        menu_text_rect = menu_text.get_rect(center=self.menu_button_rect.center)

        correct_word_font = pg.font.Font("assets/PressStart2P-vaV7.ttf", 30)
        correct_word_text1 = correct_word_font.render("The correct word is:", True, "black")
        correct_word_text1_rect = correct_word_text1.get_rect(center=(WIDTH // 2, 800))

        self.partial_correct_word = self.letter_reveal()
        print(self.word.correct_word)
        correct_word_text2 = correct_word_font.render(f"{self.partial_correct_word.upper()}", True, "black")
        correct_word_text2_rect = correct_word_text2.get_rect(center=(WIDTH // 2, 900))

        bomb_font = pg.font.Font("assets/PressStart2P-vaV7.ttf", 20)
        bomb_text = bomb_font.render("Use Bomb", True, "white")
        self.bomb_button_rect = pg.Rect(1000, 200, 200, 40)
        pg.draw.rect(SCREEN, (200, 0, 0), self.bomb_button_rect, border_radius=10)
        bomb_text_rect = bomb_text.get_rect(center=self.bomb_button_rect.center)
        bomb_count_text = bomb_font.render(f"{self.player.items['Bomb']}", True, "black")
        bomb_count_rect = bomb_count_text.get_rect(center=(1100, 265))

        mag_font = pg.font.Font("assets/PressStart2P-vaV7.ttf", 16)
        mag_text = mag_font.render("Use Magnifying Glass", True, "white")
        self.mag_button_rect = pg.Rect(900, 400, 350, 40)
        pg.draw.rect(SCREEN, (0, 200, 0), self.mag_button_rect, border_radius=10)
        mag_text_rect = mag_text.get_rect(center=self.mag_button_rect.center)
        mag_count_text = bomb_font.render(f"{self.player.items['Magnify']}", True, "black")
        mag_count_rect = mag_count_text.get_rect(center=(1100, 465))

        SCREEN.blit(header, header_rect)

        SCREEN.blit(correct_word_text1, correct_word_text1_rect)
        SCREEN.blit(correct_word_text2, correct_word_text2_rect)

        SCREEN.blit(score_text, score_text_rect)
        SCREEN.blit(level_text, level_text_rect)

        SCREEN.blit(BOMB_ICON, (self.bomb_button_rect.centerx - 55, self.bomb_button_rect.top - 105))
        SCREEN.blit(bomb_text, bomb_text_rect)
        SCREEN.blit(bomb_count_text, bomb_count_rect)

        SCREEN.blit(MAGNIFY_ICON, (self.mag_button_rect.centerx - 45, self.mag_button_rect.top - 105))
        SCREEN.blit(mag_text, mag_text_rect)
        SCREEN.blit(mag_count_text, mag_count_rect)

        SCREEN.blit(menu_text, menu_text_rect)
        pg.display.update()

    def show_invalid_word_overlay(self, word):
        previous_screen = SCREEN.copy()

        overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        overlay.fill((255, 0, 0, 128))

        font_main = pg.font.Font("assets/PressStart2P-vaV7.ttf", 30)
        font_hint = pg.font.Font("assets/PressStart2P-vaV7.ttf", 18)

        invalid_text = font_main.render(f"'{word.upper()}' is not a valid word!", True, "white")
        invalid_text_rect = invalid_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))

        hint = font_hint.render("Press any key to continue...", True, "white")
        hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        SCREEN.blit(overlay, (0, 0))
        SCREEN.blit(invalid_text, invalid_text_rect)
        SCREEN.blit(hint, hint_rect)
        pg.display.update()

        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    waiting = False
            pg.time.delay(10)
        SCREEN.blit(previous_screen, (0, 0))
        pg.display.update()

    def create_new_letter(self, key_pressed):
        self.current_guess_letter += key_pressed
        new_letter = Letter(key_pressed, (self.current_letter_bg_x, self.player.attempts * 100 + LETTER_Y_SPACING))
        self.current_letter_bg_x += LETTER_X_SPACING
        self.guesses[self.player.attempts].append(new_letter)
        self.current_guess.append(new_letter)
        for guess in self.guesses:
            for letter in guess:
                letter.draw()

    def delete_letter(self):
        self.current_guess[-1].delete()
        self.guesses[self.player.attempts].pop()
        self.current_guess.pop()
        self.current_guess_letter = self.current_guess_letter[:-1]
        self.current_letter_bg_x -= LETTER_X_SPACING

    def handle_guesses(self):
        guess_str = ''.join([letter.text for letter in self.current_guess]).lower()
        if guess_str in WORDS:
            result = self.word.check_guess(self.current_guess)
            self.game_result = result
            self.player.attempts += 1
            self.current_guess = []
            self.current_guess_letter = ""
            self.current_letter_bg_x = 432
            if result == "W":
                print("You Win!")
                self.score_calculation()
                self.player.update_score()
                self.player.level_up()
            elif self.player.attempts == 6 and result == "":
                self.game_result = "L"
                print(f"You Lose! The word was: {self.word.correct_word.upper()}")
        else:
            print(f"'{guess_str.upper()}' is not a valid word!")
            self.show_invalid_word_overlay(guess_str)

    def score_calculation(self):
        score_list = [60, 50, 40, 30, 20, 10]
        self.player.level_score = 0
        if self.player.attempts <= len(score_list):
            self.player.level_score += score_list[self.player.attempts - 1]

        correct_word = self.word.correct_word
        total_letters = len(correct_word) * self.player.attempts
        correct_letters = 0
        for guess in self.guesses[:self.player.attempts]:
            for i, letter in enumerate(guess):
                if letter.text.lower() in correct_word:
                    correct_letters += 1

        if total_letters:
            guess_accuracy = round(correct_letters / total_letters, 2)
        else:
            guess_accuracy = 0

        self.level_logs.append({
            "Level": self.player.level,
            "Score": self.player.level_score,
            "Attempts Used": self.player.attempts,
            "Guess Accuracy": guess_accuracy
        })

        return self.player.level_score

    def letter_reveal(self):
        correct_word = self.word.correct_word
        appear_index = []
        reveal_letter = []
        number_reveal = 2

        if self.player.level <= 5:
            number_reveal = random.choice([2, 3])
        elif 6 <= self.player.level <= 10:
            number_reveal = random.choice([1, 2])
        elif 11 <= self.player.level <= 19:
            number_reveal = 1
        else:
            number_reveal = 0
        while len(appear_index) < number_reveal:
            index = random.randint(0, len(correct_word) - 1)
            if index not in appear_index:
                print(correct_word[index])
                appear_index.append(index)
                reveal_letter.append(correct_word[index])

        show_word = [letter if i in appear_index else "-" for i, letter in enumerate(correct_word)]
        partial_correct_word = " ".join(show_word)

        return partial_correct_word

    def update_bomb_count(self):
        bomb_font = pg.font.Font("assets/PressStart2P-vaV7.ttf", 20)
        pg.draw.rect(SCREEN, "white", pg.Rect(1050, 250, 100, 30))
        bomb_count_text = bomb_font.render(f"{self.player.items['Bomb']}", True, "black")
        bomb_count_rect = bomb_count_text.get_rect(center=(1100, 265))
        SCREEN.blit(bomb_count_text, bomb_count_rect)
        pg.display.update(bomb_count_rect)

    def update_mag_count(self):
        mag_font = pg.font.Font("assets/PressStart2P-vaV7.ttf", 20)
        pg.draw.rect(SCREEN, "white", pg.Rect(1050, 450, 100, 50))
        mag_count_text = mag_font.render(f"{self.player.items['Magnify']}", True, "black")
        mag_count_rect = mag_count_text.get_rect(center=(1100, 465))
        SCREEN.blit(mag_count_text, mag_count_rect)
        pg.display.update(mag_count_rect)

    def update_partial_word(self):
        correct_word_font = pg.font.Font("assets/PressStart2P-vaV7.ttf", 30)
        pg.draw.rect(SCREEN, "white", pg.Rect(WIDTH // 2 - 200, 850, 400, 100))
        updated_word_text = correct_word_font.render(self.partial_correct_word.upper(), True, "black")
        updated_word_rect = updated_word_text.get_rect(center=(WIDTH // 2, 900))
        SCREEN.blit(updated_word_text, updated_word_rect)
        pg.display.update()

    def handle_bomb_button(self, pos):
        if hasattr(self, 'bomb_button_rect') and self.bomb_button_rect.collidepoint(pos):
            print("Bomb clicked!")

            if self.player.items.get("Bomb", 0) > 0:
                bomb = Bomb(self)
                bomb.apply_effect()
                if bomb.status == "T":
                    self.player.items["Bomb"] -= 1
                    self.player.item_used["Bomb"] += 1
                    self.update_bomb_count()
                print(f"Bombs left: {self.player.items['Bomb']}")
            else:
                print("No bombs left!")

    def handle_mag_button(self, pos):
        if hasattr(self, 'mag_button_rect') and self.mag_button_rect.collidepoint(pos):
            print("Magnifying Glass clicked!")

            if self.player.items.get("Magnify", 0) > 0:
                mag = Magnifying_Glass(self)
                mag.apply_effect()
                if mag.status == "T":
                    self.player.items["Magnify"] -= 1
                    self.player.item_used["Magnify"] += 1
                    self.update_mag_count()
                print(f"Magnifying Glass left: {self.player.items['Magnify']}")
            else:
                print("No Magnifying Glass left!")

    def handle_menu_button(self, pos):
        if self.menu_button_rect.collidepoint(pos):
            self.game_state = "menu"
            self.menu_display()

    def go_next_level(self):
        if self.player.level % 4 == 1:
            self.shop = Shop(self)
            self.shop.display_item()
            self.game_state = "shop"
            return

        pg.draw.rect(SCREEN, "white", (10, 750, 1000, 800))
        next_level_text = LETTER_FONT.render("Press ENTER to Go Next Level!", True, "black")
        next_level_rect = next_level_text.get_rect(center=(WIDTH / 2, 900))

        level_point_text = LETTER_FONT.render(f"Point +{self.player.level_score}!", True, "black")
        level_point_rect = level_point_text.get_rect(center=(WIDTH / 2, 850))

        SCREEN.blit(next_level_text, next_level_rect)
        SCREEN.blit(level_point_text, level_point_rect)
        pg.display.update()

    def show_game_over(self):
        previous_screen = SCREEN.copy()
        overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        SCREEN.blit(previous_screen, (0, 0))
        SCREEN.blit(overlay, (0, 0))

        popup_rect = pg.Rect(WIDTH // 2 - 350, HEIGHT // 2 - 175, 700, 350)
        pg.draw.rect(SCREEN, "white", popup_rect, border_radius=20)
        pg.draw.rect(SCREEN, "black", popup_rect, 4, border_radius=20)

        title_font = pg.font.Font("assets/PressStart2P-vaV7.ttf", 36)
        text_font = pg.font.Font("assets/PressStart2P-vaV7.ttf", 20)

        title_text = title_font.render("Game Over", True, "black")
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        SCREEN.blit(title_text, title_rect)

        correct_word_text = text_font.render(f"The word was: {self.word.correct_word.upper()}", True, "black")
        correct_word_rect = correct_word_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        SCREEN.blit(correct_word_text, correct_word_rect)

        score_text = text_font.render(f"Score: {self.player.score}", True, "black")
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        SCREEN.blit(score_text, score_rect)

        level_text = text_font.render(f"Level Reached: {self.player.level}", True, "black")
        level_rect = level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        SCREEN.blit(level_text, level_rect)

        continue_text = text_font.render("Press ENTER to return to menu", True, "black")
        continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 110))
        SCREEN.blit(continue_text, continue_rect)

        pg.display.update()

    def reset(self, new_game=False):
        SCREEN.fill("white")
        SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
        self.game_result = ""
        self.guesses = [[] for i in range(6)]
        self.current_guess = []
        self.current_guess_letter = ""
        self.current_letter_bg_x = 432
        self.player.attempts = 0
        self.word = Word()
        if new_game:
            self.player = Player()
        pg.display.update()

    def game_loop(self):
        while self.running:
            if self.game_result == "W":
                self.go_next_level()
            elif self.game_result == "L" and not self.game_over_displayed:
                self.show_game_over()
                logger = GameStats(self.level_logs, self.player, self.player.item_used)
                logger.write_logs_to_csv()
                self.game_over_displayed = True
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.game_state == "menu":
                            if self.play_button_rect.collidepoint(event.pos):
                                self.reset(new_game=True)
                                self.game_over_displayed = False
                                self.game_state = "play"
                                self.starter_display()
                            elif self.stat_button_rect.collidepoint(event.pos):
                                subprocess.Popen(["python", "visualize.py"])
                            elif self.exit_button_rect.collidepoint(event.pos):
                                pg.quit()
                                sys.exit()
                        elif self.game_state == "shop":
                            for item, rect in self.shop.buttons.items():
                                if rect.collidepoint(event.pos):
                                    self.shop.confirm_purchase(item)

                            if hasattr(self.shop, "continue_button") and self.shop.continue_button.collidepoint(
                                    event.pos):
                                self.game_state = "play"
                                self.reset(new_game=False)
                                self.starter_display()
                        elif self.game_state == "play":
                            self.handle_menu_button(event.pos)
                            self.handle_bomb_button(event.pos)
                            self.handle_mag_button(event.pos)
                if self.game_state == "play":
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            if len(self.current_guess_letter) > 0:
                                self.delete_letter()
                        elif event.key == pg.K_RETURN:
                            if self.game_result == "W":
                                self.game_over_displayed = False
                                self.reset(new_game=False)
                                self.starter_display()
                            elif self.game_result == "L":
                                self.reset(new_game=True)
                                self.menu_display()
                                self.game_state = "menu"
                                self.game_over_displayed = False
                            else:
                                if len(self.current_guess_letter) == 5:
                                    self.handle_guesses()
                        else:
                            key_pressed = event.unicode.upper()
                            if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                                if len(self.current_guess_letter) < 5:
                                    self.create_new_letter(key_pressed)
