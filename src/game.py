import pygame as pg
import pytmx

from src.constants import WINDOW_SIZE, FPS, SCALE
from src.screens.screen_manager import ScreenManager
from src.screens import MenuScreen, PlayScreen


class Game:
    def __init__(self):
        pg.init()
        pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP, pg.VIDEORESIZE])

        self.is_running = True
        self.clock = pg.time.Clock()
        self.window = pg.display.set_mode(WINDOW_SIZE, pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE)

        self.screen_manager = ScreenManager()
        self.screen_manager.set_current(MenuScreen(self.screen_manager))

    def poll_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
            if event.type == pg.VIDEORESIZE:
                self.window = pg.display.set_mode(event.size, pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE)

            self.screen_manager.current_screen.handle_input(event)

    def draw(self):
        """ Clear the screen then render all objects. """

        self.screen_manager.draw(self.window)

        pg.display.flip()

    def update(self):
        """ Update all objects.  """

        # calculate the delta time
        dt = self.clock.tick(FPS) * .001 * FPS

        self.poll_events()
        self.screen_manager.update(dt)
