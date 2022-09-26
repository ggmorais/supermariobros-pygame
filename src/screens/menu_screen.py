import pygame as pg 

from src.constants import WINDOW_SIZE
from src.screens.screen_manager import ScreenManager, Screen


class MenuScreen(Screen):
    def __init__(self, manager: ScreenManager):
        super().__init__(manager)

        self.title = pg.font.SysFont("abc", 48)

    def draw(self, target: pg.Surface):
        self.canvas.fill((0, 0, 0))

        title = self.title.render("SUPER MARIO BROS.", True, (255, 255, 255))
        self.canvas.blit(title, (WINDOW_SIZE[0] / 2 - title.get_width() / 2, WINDOW_SIZE[1] / 2 - 80))

    def update(self, dt: float):
        key_pressed = pg.key.get_pressed()

        if key_pressed[pg.K_SPACE]:
            self.manager.set_current("play")
