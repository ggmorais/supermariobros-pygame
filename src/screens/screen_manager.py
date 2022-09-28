from __future__ import annotations

import pygame as pg

from src.constants import WINDOW_SIZE


class Screen:
    def __init__(self, manager: ScreenManager):
        self.manager = manager
        self.canvas = pg.Surface(WINDOW_SIZE)
        self.rect = self.canvas.get_rect()

    def draw(self, target: pg.Surface):
        pass

    def update(self, dt: float):
        pass

    def handle_input(self, event: pg.event.Event):
        pass


class TransitionScreen(Screen):
    pass


class ScreenManager:
    def __init__(self):
        # self.screens: dict[str, Screen] = {
        #     "transition": Screen(self)
        # }
        self.transition_screen = TransitionScreen(self)
        self.screens: list[Screen] = [
            self.transition_screen
        ]
        self.current_screen = None
        self.next_screen = None

        self.is_transitioning = False
        self.next_transparency = 100

        self.timer = 0
    
    def set_current(self, screen: Screen, destroy_previous: bool = True):
        if type(self.current_screen) is screen:
            return 

        if screen not in self.screens:
            self.screens.append(screen)

        if destroy_previous and self.current_screen:
            self.screens.remove(self.current_screen)

        self.next_screen = screen
        self.current_screen = self.transition_screen
        self.is_transitioning = True

        self.timer = pg.time.get_ticks()

    def draw(self, target: pg.Surface):
        # draw the objects
        # self.get_current().draw(target)
        self.current_screen.draw(target)

        if self.is_transitioning:
            self.current_screen.canvas.set_alpha(50)
            self.next_screen.canvas.set_alpha(150)

        target.blit(pg.transform.scale(self.current_screen.canvas, target.get_rect().size), self.current_screen.rect)

    def update(self, dt: float):
        if self.is_transitioning and pg.time.get_ticks() - self.timer >= 200:
            self.next_screen.canvas.set_alpha(255)
            self.is_transitioning = False
            self.current_screen = self.next_screen
            self.timer = 0

        if not self.is_transitioning:
            self.current_screen.update(dt)
