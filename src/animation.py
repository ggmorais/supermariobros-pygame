import pygame as pg


class Animation:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.current_frame = 0
        self.timer = 0

    def play(self, name: str):
        if self.current_state == name:
            return
        self.current_state = name
        self.current_frame = 0

    def add_state(self, name: str, surfaces: list[pg.Surface], fps: int = 0):
        self.states[name] = {
            "fps": fps,
            "surfaces": surfaces
        }

    def get_current_surface(self) -> pg.Surface:
        return self.states[self.current_state]["surfaces"][self.current_frame]

    def update(self):
        state = self.states[self.current_state]

        if len(state["surfaces"]) == 1:
            return

        time_now = pg.time.get_ticks()
        time_diff = time_now - self.timer

        if int(time_diff) >= int(1000 / state["fps"]):
            self.timer = time_now

            if self.current_frame + 1 == len(state["surfaces"]):
                self.current_frame = 0
            else:
                self.current_frame += 1
