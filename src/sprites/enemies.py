import typing
import pygame as pg

from src.sprites.spritesheet import Spritesheet
from src.physics import Body
from src.animation import Animation

if typing.TYPE_CHECKING:
    from src.screens import PlayScreen


class Enemy(pg.sprite.Sprite):
    def __init__(self, play_screen: "PlayScreen", x: int, y: int, spritesheet: Spritesheet):
        super().__init__()

        self.play_screen = play_screen
        self.rect = pg.rect.Rect(x, y, 0, 0)
        self.spritesheet = spritesheet
        self.body = Body(self.rect, self.play_screen.tilemap.get_collidables())
        self.animation = Animation()

        self.define_enemy()

    def define_enemy(self):
        pass

    def draw(self, target: pg.Surface, offset: pg.math.Vector2):
        pass

    def update(self, dt: float):
        self.body.update()

    def prepare_to_die(self):
        pass


class Goomba(Enemy):
    def define_enemy(self):
        self.image = self.spritesheet.split_parse_sprite("goomba", 16)
        
        self.animation.add_state("idle", self.image[:2], 10)
        self.animation.add_state("dead", self.image[2:3], 10)
        self.animation.play("idle")
        
        self.rect.size = self.animation.get_current_surface().get_size()

        self.body.use_constant_velocity = True
        self.speedx = 2
        self.body.acceleration.x = self.speedx
        self.is_dead = False
        self.death_timer = 0

    def draw(self, target: pg.Surface, offset: pg.math.Vector2):
        target.blit(self.animation.get_current_surface(), (self.rect.x - offset.x, self.rect.y - offset.y))

    def update(self, dt: float):
        self.animation.update()

        if not self.body.on_ground:
            self.body.acceleration.x = 0
        else:
            self.body.acceleration.x = self.speedx

        if not self.is_dead:
            self.body.update(dt)
        
        if self.body.right_collision:
            # self.body.acceleration.x = -abs(self.body.acceleration.x)
            self.speedx = -abs(self.speedx)
        elif self.body.left_collision:
            # self.body.acceleration.x = abs(self.body.acceleration.x)
            self.speedx = abs(self.speedx)

        if self.is_dead:
            time_diff = pg.time.get_ticks() - self.death_timer

            # if diff greater than 1s
            if time_diff >= 1000:
                self.play_screen.enemies.remove(self)

    def prepare_to_die(self):
        self.is_dead = True
        self.death_timer = pg.time.get_ticks()
        self.animation.play("dead")
