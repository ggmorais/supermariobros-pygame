import pygame as pg

from src.constants import WINDOW_SIZE, SCALE
from src.sprites.tile import Tile
from src.sprites.spritesheet import Spritesheet
from src.animation import Animation
from src.physics import Body


class Mario(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, spritesheet: Spritesheet, collidables: list = None, collectables: pg.sprite.Group = None):
        self.spritesheet = spritesheet
        self.facing_right = True
        self.rect = None
        self.is_grown = False
        self.key_pressed = set()
        self.collectables = collectables

        self.animation = Animation()
        self.create_mario("little_mario")
        self.body = Body(self.rect, collidables)

        self.rect.x = x
        self.rect.y = y

    def draw(self, target: pg.Surface, offset: pg.math.Vector2):
        target.blit(
            pg.transform.flip(self.animation.get_current_surface(), not self.facing_right, False),
            (self.rect.x - offset.x, self.rect.y - offset.y)
        )

    def update(self, dt: float):
        self.body.update(dt)
        self.animation.animate()

        if "left" in self.key_pressed:
            self.body.acceleration.x = -.4
        elif "right" in self.key_pressed:
            self.body.acceleration.x = .4
        else:
            self.body.acceleration.x = 0

        if abs(self.body.velocity.x) >= .8 and self.body.on_ground:
            self.animation.run_state("run")
        elif self.body.on_ground:
            self.animation.run_state("idle")

        if self.body.velocity.x > 0:
            self.facing_right = True
        if self.body.velocity.x < 0:
            self.facing_right = False

        self.check_collectables()

        if self.body.head_collision:
            self.body.head_collision.on_head_hit()

    def check_collectables(self):
        if pg.sprite.spritecollide(self, self.collectables, dokill=True):
            self.grow()

    def create_mario(self, mario_sprite: str = "little_mario"):
        self.image = self.spritesheet.split_parse_sprite(mario_sprite, 16)
        self.animation.add_state("idle", self.image[0:1])
        self.animation.add_state("run", self.image[1:4], fps=16)
        self.animation.add_state("jump", self.image[5:6])
        self.animation.run_state("idle")

        if self.rect:
            self.rect.size = self.animation.get_current_surface().get_size()
            self.rect.y -= self.rect.h / 2
        else:
            self.rect = self.animation.get_current_surface().get_rect()

    def grow(self):
        if self.is_grown:
            return

        self.is_grown = True
        self.create_mario("big_mario")

    def jump(self):
        if self.body.on_ground:
            self.body.is_jumping = True
            self.body.velocity.y -= 10
            self.body.on_ground = False
            self.animation.run_state("jump")
