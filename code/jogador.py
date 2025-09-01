# jogador.py
class Jogador:
    def __init__(self, vidas=3):
        self.score = 0
        self.phase = 1
        self.lives = vidas

    def add_point(self):
        self.score += 1
        if self.score % 5 == 0:
            self.phase += 1

    def lose_life(self):
        self.lives -= 1

    def reset(self):
        self.score = 0
        self.phase = 1
        self.lives = 3
