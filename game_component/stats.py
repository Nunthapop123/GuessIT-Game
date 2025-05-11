import csv
import os


class GameStats:
    def __init__(self, level_logs, player, used_powerups):
        self.level_logs = level_logs
        self.player = player
        self.used_powerups = used_powerups
        self.data_dir = "assets/data"
        os.makedirs(self.data_dir, exist_ok=True)

    def write_logs_to_csv(self):
        self._write_level_logs()
        self._write_summary()

    def _write_level_logs(self):
        filename = os.path.join(self.data_dir, "game_log.csv")
        fieldnames = ["Level", "Score", "Attempts Used", "Guess Accuracy"]

        file_exists = os.path.isfile(filename)
        with open(filename, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            for row in self.level_logs:
                writer.writerow(row)

    def _write_summary(self):
        filename = os.path.join(self.data_dir, "game_summary.csv")
        write_header = not os.path.exists(filename)

        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            if write_header or f.tell() == 0:
                writer.writerow([
                    "Final Level", "Total Score",
                    "Bombs Used", "Magnifies Used"
                ])
            writer.writerow([
                self.player.level,
                self.player.score,
                self.used_powerups.get("Bomb", 0),
                self.used_powerups.get("Magnify", 0)
            ])