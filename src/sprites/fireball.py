import math
import typing
import pygame as pg

from src.sprites.spritesheet import Spritesheet
from src.animation import Animation
from src.constants import SCALE, WINDOW_SIZE
from src.physics import Body

if typing.TYPE_CHECKING:
    from src.sprites.mario import Mario

class Fireball(pg.sprite.Sprite):
    def __init__(self, mario: "Mario", x: int, y: int, right_side: bool = True):
        self.mario = mario
        self.image = pg.image.load("assets/gfx/fireball.png").convert_alpha()
        self.images = [
            self.image.subsurface(8 * i, 0, 8, 8)
            for i in range(1, 4)
        ]
        self.animation = Animation()
        self.animation.add_state("fire", self.images, fps=10)
        self.animation.run_state("fire")

        self.rect = self.animation.get_current_surface().get_rect()
        self.rect.x = x
        self.rect.y = y

        self.body = Body(self.rect, self.mario.game.tilemap.get_collidables())
        self.body.friction = 0
        self.body.acceleration.x = 5 if right_side else -5
        self.body.acceleration.y = 3
        self.body.use_constant_velocity = True
        self.body.use_constant_velocity_vertical = True

        self.quicks = 0

    def draw(self, target: pg.Surface, offset: pg.math.Vector2):
        target.blit(
            pg.transform.scale(self.animation.get_current_surface(), (self.rect.w * 1.5, self.rect.h * 1.5)),
            (self.rect.x - offset.x, self.rect.y - offset.y)
        )

    def update(self, dt: float):
        self.body.update(dt)

        if math.hypot(self.rect.x - self.mario.rect.x, self.rect.y - self.mario.rect.y) > WINDOW_SIZE[0] / 2 + self.mario.rect.w:
            self.mario.game.fireballs.remove(self)

        if self.quicks == 4 or self.body.right_collision or self.body.left_collision:
            self.mario.game.fireballs.remove(self)

        if self.body.on_ground:
            self.body.acceleration.y = -self.body.acceleration.y
            self.quicks += 1

        if self.body.head_collision:
            self.body.acceleration.y = 1
            self.quicks += 1

        self.check_enemies()

    def check_enemies(self):
        enemy = pg.sprite.spritecollideany(self, self.mario.game.enemies)
        if enemy and not enemy.is_dead:
            enemy.prepare_to_die()
            self.mario.game.fireballs.remove(self)
