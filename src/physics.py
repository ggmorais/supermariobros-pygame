import math
import pygame as pg


class Body:
    def __init__(self, rect: pg.Rect, collidables: list = None):
        self.is_jumping = False
        self.on_ground = False
        self.gravity = .35
        self.friction = -.12
        self.rect = rect
        self.collidables = collidables or []
        self.head_collision = None
        self.right_collision = None
        self.left_collision = None

        self.position = pg.math.Vector2(self.rect.x, self.rect.y)
        self.velocity = pg.math.Vector2(0, 0)
        self.acceleration = pg.math.Vector2(0, self.gravity)

        self.use_constant_velocity = False

    def update(self, dt: float):
        self.horizontal_movement(dt)
        self.vertical_movement(dt)

    def horizontal_movement(self, dt: float):
        if self.use_constant_velocity:
            self.velocity.x = self.acceleration.x
        else:
            self.acceleration.x += self.velocity.x * self.friction
            self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(4)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.rect.x = self.position.x

        self.check_collisions_x()

    def vertical_movement(self, dt: float):
        self.velocity.y += self.acceleration.y * dt
        
        if self.velocity.y > 7:
            self.velocity.y = 7
        
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        self.rect.bottom = self.position.y

        self.check_collisions_y()

    def limit_velocity(self, max_vel: float):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01:
            self.velocity.x = 0

    def get_hits(self, tiles) -> list:
        # keep only the closest tiles
        tiles = [
            i for i in tiles 
            if math.hypot(self.rect.x - i.rect.x, self.rect.y - i.rect.y) < 80
        ]

        for tile in tiles:
            if self.rect.colliderect(tile):
                yield tile

    def check_collisions_x(self):
        self.left_collision, self.right_collision = None, None

        for tile in self.get_hits(self.collidables):
            if self.velocity.x > 0:
                self.position.x = tile.rect.left - self.rect.w
                self.rect.x = self.position.x
                self.right_collision = tile
            if self.velocity.x < 0:
                self.position.x = tile.rect.right
                self.rect.x = self.position.x
                self.left_collision = tile
    
    def check_collisions_y(self):
        self.head_collision = None
        self.on_ground = False
        self.rect.bottom += 1

        for tile in self.get_hits(self.collidables):
            if self.velocity.y > 0:
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.rect.top
                self.rect.bottom = self.position.y
            if self.velocity.y < 0:
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.h
                self.rect.bottom = self.position.y

                self.head_collision = tile
