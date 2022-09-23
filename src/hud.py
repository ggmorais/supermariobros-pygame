import pygame as pg
from src.constants import WINDOW_SIZE


class Hud:
    def __init__(self):
        self.score = 0
        self.timer = 300
        self.time_count = 0
        
        # TODO
        # Importar uma fonte pixelada

        self.font = pg.font.SysFont("BitMap", 36)

        self.labels = {}
        self.add_label("mario", (20, 5), "MARIO")
        self.add_label("score", (20, 30), self.score)
        self.add_label("time", (400, 5), "TIME")
        self.add_label("timer", (400, 30), self.timer)

    def add_label(self, name: str, pos: tuple, initial_value: str = None):
        self.labels[name] = {
            "value": initial_value,
            "pos": pos
        }

    def draw(self, target: pg.Surface):
        for k, v in self.labels.items():
            img = self.font.render(str(v["value"]), True, (255, 255, 255))
            target.blit(img, v["pos"])

    def update(self, dt: float):
        self.time_count = int(pg.time.get_ticks() / 10 / 60)

        self.labels["score"]["value"] = self.score
        self.labels["timer"]["value"] = self.timer - self.time_count
