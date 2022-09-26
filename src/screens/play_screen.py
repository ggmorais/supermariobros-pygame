from __future__ import annotations

import typing
import pygame as pg

from src.screens.screen_manager import ScreenManager, Screen
from src.constants import WINDOW_SIZE
from src.camera import Camera, Follow, Border, Auto
from src.tilemap import Tilemap
from src.constants import WINDOW_SIZE, FPS, SCALE
from src.sprites.mario import Mario
from src.sprites.spritesheet import Spritesheet
from src.sprites.collectables import Mushroom
from src.sprites.enemies import Goomba
from src.sprites.fireball import Fireball
from src.tileset import Tileset
from src.hud import Hud


class PlayScreen(Screen):
    def __init__(self, manager: ScreenManager):
        super().__init__(manager)

        self.hud = Hud()
        self.key_pressed = set()

        self.entities_spritesheet = Spritesheet("assets/mario_and_enemies.png")
        self.collectables = pg.sprite.Group()

        self.gutter_tileset = Tileset("assets/tileset_gutter.png", size=(16, 16))
        self.tilemap = Tilemap(self, "assets/map0.tmx")
        self.fireballs: list[Fireball] = []

        self.enemies = [
            Goomba(self, 350, 300, self.entities_spritesheet, self.tilemap.get_collidables())
        ]

        self.mario = Mario(
            self,
            x=300, 
            y=300, 
            spritesheet=self.entities_spritesheet
        )

        self.camera = Camera(self.mario, self.tilemap.tmx.width * self.tilemap.tmx.tilewidth * SCALE)
        self.camera_border = Border(self.camera, self.mario)
        self.camera.set_method(self.camera_border)

    def handle_input(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.manager.set_current("menu")
            if event.key == pg.K_RIGHT:
                self.key_pressed.add("right")
            elif event.key == pg.K_LEFT:
                self.key_pressed.add("left")
            if event.key == pg.K_DOWN:
                self.key_pressed.add("down")
            if event.key == pg.K_UP:
                self.mario.jump()
            if event.key == pg.K_SPACE:
                self.mario.fireball()

        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                self.key_pressed.remove("right")
            elif event.key == pg.K_LEFT:
                self.key_pressed.remove("left")
            if event.key == pg.K_DOWN:
                self.key_pressed.remove("down")
            if event.key == pg.K_UP:
                if self.mario.body.is_jumping:
                    self.mario.body.velocity.y *= .25
                    self.mario.body.is_jumping = False

    def draw(self, target: pg.Surface):
        self.tilemap.draw(self.canvas, self.camera.offset)
        self.mario.draw(self.canvas, self.camera.offset)
        
        for enemy in self.enemies:
            enemy.draw(self.canvas, self.camera.offset)
        
        for item in self.collectables:
            item.draw(self.canvas, self.camera.offset)

        for fireball in self.fireballs:
            fireball.draw(self.canvas, self.camera.offset)

        self.hud.draw(self.canvas)

    def update(self, dt: float):
        self.mario.update(dt)

        for enemy in self.enemies:
            enemy.update(dt)
        
        for item in self.collectables:
            item.update(dt)

        for fireball in self.fireballs:
            fireball.update(dt)

        self.tilemap.update(dt)

        self.camera.scroll()
        self.hud.update(dt)
