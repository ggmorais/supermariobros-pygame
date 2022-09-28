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
    from src.screens import PlayScreen


class Mario(pg.sprite.Sprite):
    def __init__(self, play_screen: "PlayScreen", x: int, y: int, spritesheet: Spritesheet):
        self.play_screen = play_screen
        self.spritesheet = spritesheet
        self.facing_right = True
        self.rect = None
        self.is_grown = False

        self.animation = Animation()
        self.create_mario("little_mario")
        self.body = Body(self.rect, self.play_screen.tilemap.get_collidables())

        self.rect.x = x
        self.rect.y = y

        self.is_dead = False
        self.deadth_timer = 0

    def draw(self, target: pg.Surface, offset: pg.math.Vector2):
        target.blit(
            pg.transform.flip(self.animation.get_current_surface(), not self.facing_right, False),
            (self.rect.x - offset.x, self.rect.y - offset.y)
        )

    def update(self, dt: float):
        self.handle_input()

        if self.body.velocity.x > 0:
            self.facing_right = True
        if self.body.velocity.x < 0:
            self.facing_right = False

        self.body.update(dt)
        self.animation.update()
        self.check_collectables()
        self.check_enemies()

        if self.body.fall_off_map:
            self.die()

        if self.body.head_collision:
            self.body.head_collision.on_head_hit()

        if self.is_dead:
            # if 1.2s passed since Mario died
            if pg.time.get_ticks() - self.deadth_timer > 1200:
                self.play_screen.go_to_menu()


    def handle_input(self):
        if self.is_dead:
            return

        if "left" in self.play_screen.key_pressed:
            self.body.acceleration.x = -.4
        elif "right" in self.play_screen.key_pressed:
            self.body.acceleration.x = .4
        else:
            self.body.acceleration.x = 0

        if "down" in self.play_screen.key_pressed and self.is_grown and self.body.on_ground:
            self.animation.play("crouch")
            self.body.acceleration.x = 0
        elif abs(self.body.velocity.x) >= .8 and self.body.on_ground:
            self.animation.play("run")
        elif self.body.on_ground:
            self.animation.play("idle")

    def die(self):
        if self.is_dead:
            return

        self.deadth_timer = pg.time.get_ticks()
        self.animation.play("dead")
        self.body.velocity.y -= 15
        self.body.on_ground = False
        self.body.velocity.x = 0
        self.is_dead = True
        self.body.collision_enabled = False

    def take_damage(self):
        if not self.is_grown:
            self.die()
        self.is_grown = False

    def fireball(self):
        if len(self.play_screen.fireballs) == 2:
            return

        pos_x = self.rect.right if self.facing_right else self.rect.left

        self.play_screen.fireballs.append(Fireball(self, x=pos_x, y=self.rect.y, right_side=self.facing_right))

    def check_collectables(self):
        if pg.sprite.spritecollide(self, self.play_screen.collectables, dokill=True):
            self.grow()

    def check_enemies(self):
        enemy = pg.sprite.spritecollideany(self, self.play_screen.enemies)
        if enemy and not enemy.is_dead:
            # enemy head collision (do damage)
            if self.body.velocity.y > 0:
                enemy.prepare_to_die()

                # apply vertical impulse on Mario
                self.body.velocity.y -= 10
                self.animation.play("jump")
                
            # enemy lateral or bottom collision (receive damage)
            elif self.body.velocity.x != 0 or self.body.velocity.y == 0 or self.body.velocity.y < 0:
                self.die()


    def create_mario(self, mario_sprite: str = "little_mario"):
        self.image = self.spritesheet.split_parse_sprite(mario_sprite, 16)
        self.animation.add_state("idle", self.image[0:1])
        self.animation.add_state("run", self.image[1:4], fps=16)
        self.animation.add_state("jump", self.image[5:6])
        self.animation.add_state("crouch", self.image[6:7])
        self.animation.add_state("dead", self.image[6:7])
        self.animation.play("idle")

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
            self.animation.play("jump")
