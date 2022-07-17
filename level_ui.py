
import pygame
import images
from grid import Grid

class LevelUI(object):
    screen: pygame.Surface
    background: pygame.Surface
    grid: Grid

    def __init__(self, screen: pygame.Surface):
        super(LevelUI, self).__init__()
        self.screen = screen
        self.grid = None
        self.background = None

    def load_level_spec(self, level_spec: dict) -> None:
        level_index = level_spec["level"] - 1
        self.background = images.LEVEL_BG[level_index]
        self.grid = Grid(level_spec["dim"][0], level_spec["dim"][1], self.screen, images.LEVEL[level_index])
        self.grid.add_objects(level_spec["objects"])

    def handle_click(self, mouse_pos: tuple[float, float]) -> None:
        self.grid.handle_click(mouse_pos)

    def render_all(self, mouse_pos: tuple[float, float]) -> None:
        self.screen.blit(self.background, (0,0))
        self.grid.render_all(mouse_pos)