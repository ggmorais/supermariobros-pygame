from __future__ import annotations

import pygame as pg

from src.constants import WINDOW_SIZE


class Screen:
    def __init__(self, manager: ScreenManager):
        self.manager = manager
        self.canvas = pg.Surface(WINDOW_SIZE)

    def draw(self, target: pg.Surface):
        pass

    def update(self, dt: float):
        pass

    def handle_input(self, event: pg.event.Event):
        pass


class ScreenManager:
    def __init__(self):
        # self._screens = {
        #     "menu": MenuScreen(self),
        #     "play": PlayScreen(self)
        # }
        self._screens: dict[str, Screen] = {}
        self._current_screen = None

    def add(self, name: str, screen: Screen):
        self._screens[name] = screen

    def set_current(self, name: str):
        self._current_screen = name

    def get_current(self):
        return self._screens[self._current_screen]

    def draw(self, target: pg.Surface):
        self.get_current().draw(target)

        # scale the scrren if the window get resized
        target.blit(pg.transform.scale(self.get_current().canvas, target.get_rect().size), (0, 0))

    def update(self, dt: float):
        self.get_current().update(dt)
