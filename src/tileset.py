import pygame as pg

from src.constants import SCALE


class Tileset:
    def __init__(self, file, size=(32, 32), margin=1, spacing=2):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pg.image.load(file).convert()
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()

    def get_tile(self, pos: int):
        tile = self.tiles[pos]
        rect = tile.get_rect()
        return pg.transform.scale(tile, (rect.w * SCALE, rect.h * SCALE))

    def load(self):
        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing
        
        for y in range(y0, h, dy):
            for x in range(x0, w, dx):
                tile = pg.Surface(self.size)
                # tile.set_colorkey((0, 0, 0))
                tile.blit(self.image, (0, 0), (x, y, w, h))
                self.tiles.append(tile)