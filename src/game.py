import pygame as pg
import pytmx

from src.camera import Camera, Follow, Border, Auto
from src.tilemap import Tilemap
from src.constants import WINDOW_SIZE, FPS, SCALE
from src.sprites.mario import Mario
from src.sprites.spritesheet import Spritesheet
from src.sprites.mushroom import Mushroom
from src.tileset import Tileset
from src.hud import Hud


class Game:
    def __init__(self):
        pg.init()
        pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP, pg.VIDEORESIZE])

        self.is_running = True
        self.hud = Hud()

        self.clock = pg.time.Clock()
        self.window = pg.display.set_mode(WINDOW_SIZE, pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE)
        self.canvas = pg.Surface(WINDOW_SIZE)
        self.key_pressed = set()

        self.entities_spritesheet = Spritesheet("assets/mario_and_enemies.png")
        self.collectables = pg.sprite.Group()

        self.gutter_tileset = Tileset("assets/tileset_gutter.png", size=(16, 16))
        self.tilemap = Tilemap(self, "assets/map0.tmx")

        self.mario = Mario(
            x=300, 
            y=300, 
            spritesheet=self.entities_spritesheet, 
            collidables=self.tilemap.get_collidables(),
            collectables=self.collectables
        )
        self.mario.key_pressed = self.key_pressed


        self.camera = Camera(self.mario, self.tilemap.tmx.width * self.tilemap.tmx.tilewidth * SCALE)
        self.camera_border = Border(self.camera, self.mario)
        self.camera.set_method(self.camera_border)


    def poll_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
            if event.type == pg.VIDEORESIZE:
                self.window = pg.display.set_mode(event.size, pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE)

            self.handle_input(event)

    def handle_input(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.is_running = False
            if event.key == pg.K_RIGHT:
                self.key_pressed.add("right")
            elif event.key == pg.K_LEFT:
                self.key_pressed.add("left")
            if event.key == pg.K_UP:
                self.mario.jump()

        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                self.key_pressed.remove("right")
            elif event.key == pg.K_LEFT:
                self.key_pressed.remove("left")
            if event.key == pg.K_UP:
                if self.mario.body.is_jumping:
                    self.mario.body.velocity.y *= .25
                    self.mario.body.is_jumping = False

    def draw(self):
        """ Clear the screen then render all objects. """

        self.window.fill((0, 0, 0))
        self.canvas.fill((0, 0, 0))

        # render objects here
        self.tilemap.draw(self.canvas, self.camera.offset)
        self.mario.draw(self.canvas, self.camera.offset)
        
        for item in self.collectables:
            item.draw(self.canvas, self.camera.offset)

        self.hud.draw(self.canvas)
     
        # scale window if it gets resized
        self.window.blit(pg.transform.scale(self.canvas, self.window.get_rect().size), (0, 0))

        pg.display.flip()

    def update(self):
        """ Update all objects.  """

        # calculate the delta time
        dt = self.clock.tick(FPS) * .001 * FPS

        self.poll_events()
        self.mario.update(dt)
        
        for item in self.collectables:
            item.update(dt)

        self.camera.scroll()
        self.hud.update(dt)

        print(f"FPS: {self.clock.get_fps()}")
