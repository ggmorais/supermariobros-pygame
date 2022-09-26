from __future__ import annotations

import typing
import pygame as pg

from src.constants import SCALE
from src.sprites.collectables import Mushroom


if typing.TYPE_CHECKING:
    from src.screens.play_screen import PlayScreen


class Tile(pg.sprite.Sprite):
    def __init__(self, play_screen: "PlayScreen", x: int, y: int, image: pg.Surface, name: str, is_collidable: bool = False, zorder: int = 0):
        super().__init__()

        self.play_screen = play_screen
        self.image = image
        self.is_collidable = is_collidable
        self.name = name
        self.zorder = zorder

        self.rect = self.image.get_rect()
        self.image = pg.transform.scale(self.image, (self.rect.w * SCALE, self.rect.h * SCALE))
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

        self.rect.x = x
        self.rect.y = y

        self.active = True

    def draw(self, target: pg.Surface, offset: pg.math.Vector2):
        target.blit(self.image, (self.rect.x - offset.x, self.rect.y - offset.y))

    def update(self, dt: float):
        pass

    def on_head_hit(self):
        pass


class MushroomBrickTile(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.animation_timer = 0
    
    def on_head_hit(self):
        self.rect.y -= 4
        self.animation_timer = pg.time.get_ticks()

        if self.active:
            self.active = False
            self.play_screen.collectables.add(Mushroom(
                self.play_screen, 
                self.rect.x, 
                self.rect.y - self.rect.h, 
                self.play_screen.entities_spritesheet
            ))
            self.image = self.play_screen.gutter_tileset.get_tile(27)
    
    def update(self, dt: float):
        if self.animation_timer != 0 and pg.time.get_ticks() - self.animation_timer >= 200:
            self.rect.y += 4
            self.animation_timer = 0


class CoinTile(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_pos_y = self.rect.y

    def update(self, dt: float):
        if self.start_pos_y - self.rect.y < self.rect.h + 20:
            # apply a slowing effect to the coin as it moves to the top
            speed_weight = (self.rect.y + (self.rect.y - self.rect.h)) / (self.start_pos_y + (self.start_pos_y - self.rect.h))
            if speed_weight < .85:
                speed_weight = .05
            self.rect.y -= 5 * speed_weight
        else:
            self.play_screen.tilemap.tiles.remove(self)


class CoinBrickTile(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.animation_timer = 0
    
    def on_head_hit(self):
        self.rect.y -= 4
        self.animation_timer = pg.time.get_ticks()

        if self.active:
            self.active = False
            self.play_screen.hud.score += 1
            self.image = self.play_screen.gutter_tileset.get_tile(27)

            coin_img = self.play_screen.gutter_tileset.get_tile(57, False)
            coin_tile = CoinTile(self.play_screen, self.rect.x, self.rect.y, image=coin_img, name="coin", is_collidable=False, zorder=3)
            self.play_screen.tilemap.tiles.append(coin_tile)

    def update(self, dt: float):
        if self.animation_timer != 0 and pg.time.get_ticks() - self.animation_timer >= 200:
            self.rect.y += 4
            self.animation_timer = 0
