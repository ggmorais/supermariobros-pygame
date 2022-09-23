import random
import pygame as pg

from src.sprites.spritesheet import Spritesheet
from src.physics import Body


class Mushroom(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, spreadsheet: Spritesheet, collidables: list = None):
        super().__init__()
        self.image = spreadsheet.parse_sprite("mushroom")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.body = Body(self.rect, collidables)
        self.body.use_constant_velocity = True
        self.body.gravity = .8

        # randomize which side that the mushroom will initially move
        self.body.acceleration.x = 2 * [-1, 1][random.randint(0, 1)]

    def draw(self, target: pg.Surface, offset: float):
        target.blit(self.image, (self.rect.x - offset.x, self.rect.y - offset.y))

    def update(self, dt: float):
        self.body.update(dt)

        if self.body.right_collision:
            self.body.acceleration.x = -abs(self.body.acceleration.x)
        elif self.body.left_collision:
            self.body.acceleration.x = abs(self.body.acceleration.x)

