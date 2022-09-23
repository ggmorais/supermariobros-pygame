from __future__ import annotations
import pygame as pg

from src.constants import SCALE
from src.sprites.mushroom import Mushroom

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.game import Game 


class Tile(pg.sprite.Sprite):
    def __init__(self, game: Game, x: int, y: int, image: pg.Surface, name: str, is_collidable: bool = False):
        self.image = image
        self.is_collidable = is_collidable
        self.name = name
        self.game = game

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


class MushroomTile(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def on_head_hit(self):
        if self.active:
            self.game.collectables.add(Mushroom(self.rect.x, self.rect.y - self.rect.h, self.game.entities_spritesheet, self.game.tilemap.get_collidables()))
            self.image = self.game.gutter_tileset.get_tile(27)
            self.active = False

class CoinTile(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def on_head_hit(self):
        if self.active:
            self.game.hud.score += 1
            self.image = self.game.gutter_tileset.get_tile(27)
            self.active = False
