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
    def __init__(self):
        self.score = 0
        self.level = 1
        self.attempts = 0
        self.items = {"Bomb": 2, "Magnify": 4}
        self.item_used = []
        self.correct_guess_count = 0
        self.total_guess = 0
        self.level_score = 0

    def update_score(self):
        self.score += self.level_score

    def level_up(self):
        self.level += 1

    def use_power_up(self, item_name):
        pass


class Item:
    def __init__(self, game_manager):
        self.name = ""
        self.effect = ""
        self.game_manager = game_manager

    def apply_effect(self):
        pass

    def get_item_details(self):
        pass


class Bomb(Item):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.name = "Bomb"
        self.effect = "Restore the latest row of guesses"
        self.status = ""

    def apply_effect(self):
        if self.game_manager.guesses_count > 0:
            self.status = "T"
            for letter in self.game_manager.guesses[self.game_manager.guesses_count - 1]:
                letter.delete()

            self.game_manager.guesses[self.game_manager.guesses_count - 1] = []
            self.game_manager.guesses_count -= 1
            print("Bomb used! Retry the last guesses!.")
        else:
            self.status = "F"
            print("No guess to undo!")


class Magnifying_Glass(Item):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.name = "Magnifying Glass"
        self.effect = "Reveal"
        self.status = ""

    def apply_effect(self):
        correct_word = self.game_manager.word.correct_word
        partial = list(self.game_manager.partial_correct_word)

        unrevealed_display_indices = []
        correct_index = 0
        for i, char in enumerate(partial):
            if char != ' ':
                if char == '-':
                    unrevealed_display_indices.append((i, correct_index))
                correct_index += 1

        if unrevealed_display_indices:
            self.status = "T"
            chosen_display_index, chosen_correct_index = random.choice(unrevealed_display_indices)
            partial[chosen_display_index] = correct_word[chosen_correct_index]
            self.game_manager.partial_correct_word = ''.join(partial)
            self.game_manager.update_partial_word()
        else:
            self.status = "F"
            print("All letters already revealed!")


class Shop:
    pass


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
        self.guesses_count = 0
        self.running = True
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
        self.bomb_button_rect = pg.Rect(1000, 100, 200, 40)
        pg.draw.rect(SCREEN, (200, 0, 0), self.bomb_button_rect, border_radius=10)
        bomb_text_rect = bomb_text.get_rect(center=self.bomb_button_rect.center)
        bomb_count_text = bomb_font.render(f"{self.player.items['Bomb']}", True, "black")
        bomb_count_rect = bomb_count_text.get_rect(center=(1100, 165))

        mag_font = pg.font.Font("assets/PressStart2P-vaV7.ttf", 16)
        mag_text = mag_font.render("Use Magnifying Glass", True, "white")
        self.mag_button_rect = pg.Rect(900, 200, 350, 40)
        pg.draw.rect(SCREEN, (0, 200, 0), self.mag_button_rect, border_radius=10)
        mag_text_rect = mag_text.get_rect(center=self.mag_button_rect.center)
        mag_count_text = mag_font.render(f"{self.player.items['Magnify']}", True, "black")
        mag_count_rect = mag_count_text.get_rect(center=(1100, 265))

        SCREEN.blit(header, header_rect)

        SCREEN.blit(correct_word_text1, correct_word_text1_rect)
        SCREEN.blit(correct_word_text2, correct_word_text2_rect)

        SCREEN.blit(score_text, score_text_rect)
        SCREEN.blit(level_text, level_text_rect)

        SCREEN.blit(bomb_text, bomb_text_rect)
        SCREEN.blit(bomb_count_text, bomb_count_rect)

        SCREEN.blit(mag_text, mag_text_rect)
        SCREEN.blit(mag_count_text, mag_count_rect)

        SCREEN.blit(menu_text, menu_text_rect)
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
                self.score_calculation()
                self.player.update_score()
                self.player.level_up()
            elif self.guesses_count == 6 and result == "":
                self.game_result = "L"
                print(f"You Lose! The word was: {self.word.correct_word.upper()}")
        else:
            print(f"'{guess_str.upper()}' is not a valid word!")

    def score_calculation(self):
        score_list = [60, 50, 40, 30, 20, 10]
        self.player.level_score = 0
        if self.guesses_count <= len(score_list):
            self.player.level_score += score_list[self.guesses_count - 1]
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
        pg.draw.rect(SCREEN, "white", pg.Rect(1050, 150, 200, 30))
        bomb_count_text = bomb_font.render(f"{self.player.items['Bomb']}", True, "black")
        bomb_count_rect = bomb_count_text.get_rect(center=(1100, 165))
        SCREEN.blit(bomb_count_text, bomb_count_rect)
        pg.display.update(bomb_count_rect)

    def update_mag_count(self):
        mag_font = pg.font.Font("assets/PressStart2P-vaV7.ttf", 20)
        pg.draw.rect(SCREEN, "white", pg.Rect(1050, 240, 100, 50))
        mag_count_text = mag_font.render(f"{self.player.items['Magnify']}", True, "black")
        mag_count_rect = mag_count_text.get_rect(center=(1100, 265))
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
                    self.update_mag_count()
                print(f"Magnifying Glass left: {self.player.items['Magnify']}")
            else:
                print("No Magnifying Glass left!")

    def handle_menu_button(self, pos):
        if self.menu_button_rect.collidepoint(pos):
            self.game_state = "menu"
            self.menu_display()

    def go_next_level(self):
        pg.draw.rect(SCREEN, "white", (10, 750, 1000, 800))
        next_level_text = LETTER_FONT.render("Press ENTER to Go Next Level!", True, "black")
        next_level_rect = next_level_text.get_rect(center=(WIDTH / 2, 900))

        level_point_text = LETTER_FONT.render(f"Point +{self.player.level_score}!", True, "black")
        level_point_rect = level_point_text.get_rect(center=(WIDTH / 2, 850))

        SCREEN.blit(next_level_text, next_level_rect)
        SCREEN.blit(level_point_text, level_point_rect)
        pg.display.update()

    # def play_again(self):
    #     pg.draw.rect(SCREEN, "white", (10, 800, 1000, 800))
    #     play_again_font = LETTER_FONT
    #     play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "black")
    #     play_again_rect = play_again_text.get_rect(center=(WIDTH / 2, 900))
    #     corrected_word_text = play_again_font.render(f"The word was {self.word.correct_word}!", True, "black")
    #     corrected_word_rect = corrected_word_text.get_rect(center=(WIDTH / 2, 850))
    #     SCREEN.blit(corrected_word_text, corrected_word_rect)
    #     SCREEN.blit(play_again_text, play_again_rect)
    #     pg.display.update()

    def reset(self, new_game=False):
        SCREEN.fill("white")
        SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
        self.game_result = ""
        self.guesses = [[]] * 6
        self.current_guess = []
        self.current_guess_letter = ""
        self.current_letter_bg_x = 432
        self.guesses_count = 0
        self.word = Word()
        if new_game:
            self.player = Player()
        pg.display.update()

    def game_loop(self):
        while self.running:
            if self.game_result != "":
                self.go_next_level()
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
                                self.game_state = "play"
                                self.starter_display()
                            if self.exit_button_rect.collidepoint(event.pos):
                                pg.quit()
                                sys.exit()
                        else:
                            self.handle_menu_button(event.pos)
                            self.handle_bomb_button(event.pos)
                            self.handle_mag_button(event.pos)
                if self.game_state == "play":
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            if len(self.current_guess_letter) > 0:
                                self.delete_letter()
                        elif event.key == pg.K_RETURN:
                            if self.game_result != "":
                                self.reset(new_game=False)
                                self.starter_display()
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
