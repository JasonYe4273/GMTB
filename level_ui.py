
import pygame
from grid import Grid

class LevelUI(object):
    screen: pygame.Surface
    grid: Grid

    def __init__(self, screen: pygame.Surface):
        super(LevelUI, self).__init__()
        self.screen = screen

    def load_level_spec(self, level_spec: dict) -> None:
        self.grid = Grid(level_spec["dim"][0], level_spec["dim"][1], self.screen)
        self.grid.add_objects(level_spec["objects"])

    def handle_click(self, mouse_pos: tuple[float, float]) -> None:
        self.grid.handle_click(mouse_pos)

    def render_all(self, mouse_pos: tuple[float, float]) -> None:
        self.grid.render_all(mouse_pos)