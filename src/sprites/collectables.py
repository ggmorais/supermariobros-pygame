import typing
import random
import pygame as pg

from src.sprites.spritesheet import Spritesheet
from src.physics import Body

if typing.TYPE_CHECKING:
    from src.screens import PlayScreen
    from src.sprites.tile import Tile


class Collectable(pg.sprite.Sprite):
    def __init__(self, play_screen: "PlayScreen", x: int, y: int, spritesheet: Spritesheet):
        super().__init__()

        self.play_screen = play_screen
        self.spritesheet = spritesheet
        self.rect = pg.rect.Rect(x, y, 0, 0)

        self.body = Body(self.rect, self.play_screen.tilemap.get_collidables())

        self.define_collectable()

    def define_collectable(self):
        pass

    def draw(self, target: pg.Surface, offset: float):
        target.blit(self.image, (self.rect.x - offset.x, self.rect.y - offset.y))

    def update(self, dt: float):
        self.body.update(dt)


class Mushroom(Collectable):
    def define_collectable(self):
        self.image = self.spritesheet.parse_sprite("mushroom")
        self.rect.size = self.image.get_size()

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

