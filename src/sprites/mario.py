import typing
import pygame as pg

from src.constants import WINDOW_SIZE, SCALE
from src.sprites.tile import Tile
from src.sprites.spritesheet import Spritesheet
from src.sprites.enemies import Enemy
from src.sprites.fireball import Fireball
from src.animation import Animation
from src.physics import Body

if typing.TYPE_CHECKING:
    from src.game import Game


class Mario(pg.sprite.Sprite):
    def __init__(self, game: "Game", x: int, y: int, spritesheet: Spritesheet):
        self.game = game
        self.spritesheet = spritesheet
        self.facing_right = True
        self.rect = None
        self.is_grown = False

        self.animation = Animation()
        self.create_mario("little_mario")
        self.body = Body(self.rect, self.game.tilemap.get_collidables())

        self.rect.x = x
        self.rect.y = y

    def draw(self, target: pg.Surface, offset: pg.math.Vector2):
        target.blit(
            pg.transform.flip(self.animation.get_current_surface(), not self.facing_right, False),
            (self.rect.x - offset.x, self.rect.y - offset.y)
        )

    def update(self, dt: float):
        if "left" in self.game.key_pressed:
            self.body.acceleration.x = -.4
        elif "right" in self.game.key_pressed:
            self.body.acceleration.x = .4
        else:
            self.body.acceleration.x = 0

        if "down" in self.game.key_pressed and self.is_grown and self.body.on_ground:
            self.animation.run_state("crouch")
            self.body.acceleration.x = 0
        elif abs(self.body.velocity.x) >= .8 and self.body.on_ground:
            self.animation.run_state("run")
        elif self.body.on_ground:
            self.animation.run_state("idle")

        if self.body.velocity.x > 0:
            self.facing_right = True
        if self.body.velocity.x < 0:
            self.facing_right = False

        self.body.update(dt)
        self.animation.animate()
        self.check_collectables()
        self.check_enemies()

        if self.body.head_collision:
            self.body.head_collision.on_head_hit()

    def fireball(self):
        if len(self.game.fireballs) == 2:
            return

        pos_x = self.rect.right if self.facing_right else self.rect.left

        self.game.fireballs.append(Fireball(self, x=pos_x, y=self.rect.y, right_side=self.facing_right))

    def check_collectables(self):
        if pg.sprite.spritecollide(self, self.game.collectables, dokill=True):
            self.grow()

    def check_enemies(self):
        enemy = pg.sprite.spritecollideany(self, self.game.enemies)
        if enemy and not enemy.is_dead:
            # enemy head collision (do damage)
            if self.body.velocity.y > 0:
                enemy.prepare_to_die()

                # apply vertical impulse on Mario
                self.body.velocity.y -= 10
                self.animation.run_state("jump")
                
            # enemy lateral or bottom collision (receive damage)
            elif self.body.velocity.x != 0 or self.body.velocity.y == 0:
                pass
            elif self.body.velocity.y < 0:
                pass


    def create_mario(self, mario_sprite: str = "little_mario"):
        self.image = self.spritesheet.split_parse_sprite(mario_sprite, 16)
        self.animation.add_state("idle", self.image[0:1])
        self.animation.add_state("run", self.image[1:4], fps=16)
        self.animation.add_state("jump", self.image[5:6])
        self.animation.add_state("crouch", self.image[6:7])
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
