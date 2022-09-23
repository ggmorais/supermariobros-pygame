import os
import csv
import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        super().__init__()

