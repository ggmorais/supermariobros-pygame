from __future__ import annotations

import pygame as pg

from abc import ABC, abstractmethod
from src.constants import WINDOW_SIZE
from src.sprites.mario import Mario



class Camera:
    def __init__(self, mario: Mario, map_width: float):
        self.mario = mario
        self.map_width = map_width
        self.offset = pg.math.Vector2(0, 0)
        self.offset_float = pg.math.Vector2(0, 0)
        self.const = pg.math.Vector2(-WINDOW_SIZE[0] / 2 + self.mario.rect.w / 2, -WINDOW_SIZE[1])
    
    def set_method(self, method: CameraScroll):
        self.method = method

    def scroll(self):
        self.method.scroll()


class CameraScroll(ABC):
    def __init__(self, camera: Camera, mario: Mario):
        self.camera = camera
        self.mario = mario

    @abstractmethod
    def scroll(self):
        pass


class Follow(CameraScroll):
    def __init__(self, camera: Camera, mario: Mario):
        super().__init__(camera, mario)

    def scroll(self):
        self.camera.offset_float.x += (self.mario.rect.x - self.camera.offset_float.x + self.camera.const.x)
        self.camera.offset_float.y += (self.mario.rect.y - self.camera.offset_float.y + self.camera.const.y)
        self.camera.offset.x = int(self.camera.offset_float.x)
        self.camera.offset.y = int(self.camera.offset_float.y)


class Border(CameraScroll):
    def __init__(self, camera: Camera, mario: Mario):
        super().__init__(camera, mario)

    def scroll(self):
        self.camera.offset_float.x += (self.mario.rect.x - self.camera.offset_float.x + self.camera.const.x)
        self.camera.offset_float.y += (self.mario.rect.y - self.camera.offset_float.y + self.camera.const.y)
        self.camera.offset.x = int(self.camera.offset_float.x)
        self.camera.offset.y = int(self.camera.offset_float.y)
        self.camera.offset.x = max(0, self.camera.offset.x)
        self.camera.offset.x = min(self.camera.offset.x, self.camera.map_width - WINDOW_SIZE[0])

        self.camera.offset.y = max(0, self.camera.offset.y)
        self.camera.offset.y = min(self.camera.offset.y, 0)


class Auto(CameraScroll):
    def __init__(self, camera: Camera, mario: Mario):
        super().__init__(camera, mario)

    def scroll(self):
        self.camera.offset.x += 1
