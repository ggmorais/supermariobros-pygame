import pygame as pg
import pytmx

from typing import TYPE_CHECKING
from src.sprites.tile import Tile, CoinBrickTile, MushroomBrickTile
from src.constants import SCALE

if TYPE_CHECKING:
    from src.screens.play_screen import PlayScreen


tiles_classes = {
    "mushroom": MushroomBrickTile,
    "coin": CoinBrickTile
}


class Tilemap:
    def __init__(self, play_screen: "PlayScreen", tmx_file: str):
        self.play_screen = play_screen
        self.tmx = pytmx.load_pygame(tmx_file)
        self.tiles: list[Tile] = []

        self.generate_tile_objects()
    
    def get_collidables(self):
        return [tile for tile in self.tiles if tile.is_collidable]

    def generate_tile_objects(self):
        for idx, layer in enumerate(self.tmx.visible_layers):
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_surface = self.tmx.get_tile_image_by_gid(gid)
                    if tile_surface:
                        tile_class = tiles_classes.get(layer.name, Tile)
                        self.tiles.append(tile_class(
                            self.play_screen,
                            x=x * self.tmx.tilewidth * SCALE, 
                            y=y * self.tmx.tileheight * SCALE, 
                            image=tile_surface,
                            name=layer.name,
                            is_collidable=layer.properties.get("collidable", False),
                            zorder=idx
                        ))

    def draw(self, target: pg.Surface, offset: pg.math.Vector2):
        for tile in sorted(self.tiles, key=lambda x: x.zorder):
            tile.draw(target, offset)

    def update(self, dt: float):
        for tile in self.tiles:
            tile.update(dt)
