import random

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
        if self.game_manager.player.attempts > 0:
            self.status = "T"
            for letter in self.game_manager.guesses[self.game_manager.player.attempts - 1]:
                letter.delete()

            self.game_manager.guesses[self.game_manager.player.attempts - 1] = []
            self.game_manager.player.attempts -= 1
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