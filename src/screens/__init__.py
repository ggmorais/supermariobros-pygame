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


class MenuScreen(Screen):
    def __init__(self, manager: ScreenManager):
        super().__init__(manager)

        self.background = pg.image.load("assets/menu_background2.png")
        self.menu_options = [
            "START",
            "SOUND",
            "EXIT"
        ]
        self.selected_option_idx = 0
        self.key_pressed_timer = 0

    def draw(self, target: pg.Surface):
        self.canvas.fill((0, 0, 0))
        self.canvas.blit(pg.transform.scale(self.background, WINDOW_SIZE), self.rect)

        for idx, name in enumerate(self.menu_options):
            color = (255, 200, 200) if idx == self.selected_option_idx else (255, 255, 255)
            img = pg.font.SysFont("", 22).render(name, False, color)
            self.canvas.blit(img, (WINDOW_SIZE[0] / 2 - img.get_width() / 2, 180 + 16 * idx))

    def update(self, dt: float):
        print(self.key_pressed_timer)
        time_now = pg.time.get_ticks()
        if self.key_pressed_timer > 0:
            if time_now - self.key_pressed_timer > 200:
                self.key_pressed_timer = 0
            else:
                return

        key_pressed = pg.key.get_pressed()

        if any(key_pressed):
            self.key_pressed_timer = pg.time.get_ticks()

        if key_pressed[pg.K_RETURN]:
            if self.menu_options[self.selected_option_idx] == "START":
                self.manager.set_current(PlayScreen(self.manager))
            if self.menu_options[self.selected_option_idx] == "EXIT":
                self.manager.game.is_running = False
        elif key_pressed[pg.K_DOWN] and self.selected_option_idx < len(self.menu_options) - 1:
            self.selected_option_idx += 1
        elif key_pressed[pg.K_UP] and self.selected_option_idx > 0:
            self.selected_option_idx -= 1


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
            Goomba(self, 100, 16, self.entities_spritesheet)
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

    def go_to_menu(self):
        self.manager.set_current(MenuScreen(self.manager))

    def handle_input(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                # self.manager.set_current("menu")
                self.manager.set_current(MenuScreen(self.manager))
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
