import json
import pygame as pg

from src.constants import SCALE


class Spritesheet:
    def __init__(self, filename: str):
        self.filename = filename
        self.spritesheet = pg.image.load(filename).convert_alpha()
        
        with open(filename.replace(".png", ".json"), "r") as f:
            self.metadata = json.load(f)

    def get_sprite(self, x: int, y: int, w: int, h: int):
        """ Return a single Surface from cordenates of the image. """

        sprite = pg.Surface((w, h), pg.SRCALPHA)
        sprite.blit(self.spritesheet, (0, 0), (x, y, w, h))
        rect = sprite.get_rect()

        return pg.transform.scale(sprite, (rect.w * SCALE, rect.h * SCALE))

    def parse_sprite(self, name: str):
        """ Return a single Surface searching the cordenates by name. """

        sprite = self.metadata[name]
        x, y = sprite["xy"]
        w, h = sprite["size"]

        return self.get_sprite(x, y, w, h)

    def split_parse_sprite(self, name: str, tile_width: int) -> list[pg.Surface]:
        """ Return multiple Surfaces by spliting the image according to the coordenates. """

        sprite = self.metadata[name]
        x, y = sprite["xy"]
        w, h = sprite["size"]

        sprites = []

        for i in range(x, x + w, tile_width):
            sprite = self.get_sprite(i, y, tile_width, h)
            sprites.append(sprite)

        return sprites
