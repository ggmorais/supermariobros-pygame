import pygame as pg
import pytmx

from typing import TYPE_CHECKING
from src.sprites.tile import CoinTile, Tile, MushroomTile
from src.constants import SCALE

if TYPE_CHECKING:
    from src.game import Game 


tiles_classes = {
    "mushroom": MushroomTile,
    "coin": CoinTile
}


class Tilemap:
    def __init__(self, game: "Game", tmx_file: str):
        self.game = game
        self.tmx = pytmx.load_pygame(tmx_file)
        self.tiles: list[Tile] = []

        self.generate_tile_objects()
    
    def get_collidables(self):
        return [tile for tile in self.tiles if tile.is_collidable]

    def generate_tile_objects(self):
        for layer in self.tmx.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_surface = self.tmx.get_tile_image_by_gid(gid)
                    if tile_surface:
                        tile_class = tiles_classes.get(layer.name, Tile)
                        self.tiles.append(tile_class(
                            self.game,
                            x=x * self.tmx.tilewidth * SCALE, 
                            y=y * self.tmx.tileheight * SCALE, 
                            image=tile_surface,
                            name=layer.name,
                            is_collidable=layer.properties.get("collidable", False)
                        ))

    def draw(self, target: pg.Surface, offset: pg.math.Vector2):
        for tile in self.tiles:
            tile.draw(target, offset)
