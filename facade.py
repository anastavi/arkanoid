import os

from model import Brick

class GameFacade:
    def __init__(self):
        self.level = None
        self.levels = []
        self.high_scores = []

    def load_level(self, level):
        self.level = level

    def load_levels(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                level = Level(os.path.join(directory, filename))
                self.levels.append(level)

    def load_high_scores(self, scores_file):
        self.high_scores = []
        try:
            with open(scores_file, "r") as file:
                for line in file:
                    name, score, level = line.strip().split(",")
                    self.high_scores.append((name, int(score), level))
        except FileNotFoundError:
            self.high_scores = []

    def save_high_score(self, player_name, score):
        level_name = os.path.splitext(os.path.basename(self.level.filename))[0]
        self.high_scores.append((player_name, score, level_name))
        self.high_scores.sort(key=lambda x: x[1], reverse=True)
        self.high_scores = self.high_scores[:5]

        with open("high_scores.txt", "w", encoding='utf-8') as file:
            for name, score, level in self.high_scores:
                file.write(f"{name},{score}, {level}\n")

    def get_high_scores(self):
        return self.high_scores

class Level:
    def __init__(self, filename):
        self.filename = filename
        self.bricks = []
        self.load_level()

    def load_level(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == 'X':
                    brick = Brick(x * 50, y * 20, 50, 20, hp=1)
                    self.bricks.append(brick)