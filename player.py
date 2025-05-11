class Player:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.attempts = 0
        self.items = {"Bomb": 2, "Magnify": 3}
        self.item_used = {"Bomb": 0, "Magnify": 0}
        self.level_score = 0

    def update_score(self):
        self.score += self.level_score

    def level_up(self):
        self.level += 1