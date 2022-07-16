import numpy
import math
import pygame
from game_object import Object, Empty

class Direction:
    X = 0
    Y = 1
    R = 2

DIRECTIONS = [Direction.X, Direction.Y, Direction.R]


class Triangle:
    o: Object
    x: int
    y: int

    def __init__(self, x_loc: int, y_loc: int, rad: int):
        self.o = Empty(x_loc, y_loc, rad)
        self.x = x_loc
        self.y = y_loc

    def get_object(self) -> Object:
        return self.o

    def set_object(self, obj: Object) -> None:
        self.o = obj

    def is_empty(self) -> bool:
        return typeof(self.o) == Empty

    def render(self, screen: pygame.Surface, left_corner: tuple[float, float]) -> None:
        self.o.render(screen, left_corner)


class Grid:
    grid: any
    unit: float
    bl: tuple[float, float]

    def __init__(self, width: int, height: int):
        self.grid = numpy.full((width, height, 2), None)
        for i in range(width):
            for j in range(height):
                for r in range(2):
                    self.grid[i, j, r] = Triangle(i, j, r)

    def _verify_coord(x: int, y: int, r: int, raise_if_bad: bool=True) -> bool:
        if x < 0 or x >= self.grid.shape[0]:
            if raise_if_bad:
                raise Exception("x coordinate out of bounds")
            return False
        if y < 0 or y >= self.grid.shape[1]:
            if raise_if_bad:
                raise Exception("y coordinate out of bounds")
            return False
        if r < 0 or r > 1:
            if raise_if_bad:
                raise Exception("r coordinate out of bounds")
            return False
        return True

    def _add_dir(x: int, y: int, r: int, d: int) -> tuple[int, int, int]:
        if d == Direction.R:
            return (x, y, 1-r)

        pm = 1 if r == 1 else -1
        if d == Direction.X:
            return (x+pm, y, 1-r)
        if d == Direction.Y:
            return (x, y+pm, 1-r)

    def shape(self) -> tuple[int, int]:
        return (self.grid.shape[0], self.grid.shape[1])

    def get_triangle(self, x: int, y: int, r: int) -> Object:
        _verify_coord(x, y, r)
        return self.grid[x, y, r]

    def get_object(self, x: int, y: int, r: int) -> Object:
        _verify_coord(x, y, r)
        return self.grid[x, y, r].get_object(o)

    def set_object(self, o: Object, x: int, y: int, r: int) -> None:
        _verify_coord(x, y, r)
        self.grid[x, y, r].set_object(o)

    def grid_adj(self, x: int, y: int, r: int) -> set[Direction]:
        _verify_coord(x, y, r)
        adj: set[Direction] = set()

        for d in DIRECTIONS:
            (x2, y2, r2) = _add_dir(x, y, r, d)
            if _verify_coord(x2, y2, r2, False):
                adj.add(d)
        return adj

    def move_object(self, x: int, y: int, r: int, d: int) -> None:
        _verify_coord(x,y,r)
        o = self.grid[x, y, r].get_object()

        (x2, y2, r2) = _add_dir(x, y, r, d)
        _verify_coord(x2, y2, r2)

        if not _self.grid[x2, y2, r2].is_empty():
            raise Exception(f"Cannot move from ({x}, {y}, {r}) into nonempty space at ({x2}, {y2}, {r2})")

        o.move(d)
        self.grid[x2, y2, r2].set_object(o)
        self.grid[x, y, r].set_object(Empty())


    def grid_to_screen_coord(self, x: int, y: int, r: int) -> tuple[float, float]:
        rhombus_bl = (self.bl[0] + 2*x*self.unit + y*self.unit, self.bl[1] - math.sqrt(3)*y*self.unit)

        if r == 0:
            return rhombus_bl
        else:
            return (rhombus_bl[0] + self.unit, rhombus_bl[1] + math.sqrt(3)*self.unit)

    def render_all(self, screen: pygame.Surface) -> None:
        MARGIN = 200

        (screen_w, screen_h) = screen.get_size()
        (adj_w, adj_h) = (screen_w - MARGIN, screen_h - MARGIN)
        (grid_x, grid_y) = self.shape()
        x = 2*grid_x + grid_y
        y = math.sqrt(3)*grid_y

        self.unit = min(adj_w / x, adj_h / y)
        grid_w = self.unit * x
        grid_h = self.unit * y

        self.bl = ((screen_w - grid_w) / 2, (screen_h + grid_h) / 2)

        # Draw horizontals
        for j in range(grid_y+1):
            x_offset = 2*grid_x*self.unit
            y_offset = j*self.unit
            pygame.draw.line(
                screen,
                (0,0,0),
                (self.bl[0] + y_offset, self.bl[1] - math.sqrt(3)*y_offset),
                (self.bl[0] + y_offset + x_offset, self.bl[1] - math.sqrt(3)*y_offset)
            )

        # Draw long diagonals
        for i in range(grid_x+1):
            x_offset = 2*i*self.unit
            y_offset = grid_y*self.unit
            pygame.draw.line(
                screen,
                (0,0,0),
                (self.bl[0] + x_offset, self.bl[1]),
                (self.bl[0] + x_offset + y_offset, self.bl[1] - math.sqrt(3)*y_offset)
            )

        # Draw first half of cross diagonals
        for i in range(grid_x):
            offset = i*self.unit
            pygame.draw.line(
                screen,
                (0,0,0),
                (self.bl[0] + 2*offset, self.bl[1]),
                (self.bl[0] + offset, self.bl[1] - math.sqrt(3)*offset),
            )

        for i in range(grid_y):
            br = (self.bl[0] + 2*grid_x*self.unit, self.bl[1])
            tl = (self.bl[0] + grid_y*self.unit, self.bl[1] - math.sqrt(3)*grid_y*self.unit)

            offset = i*self.unit
            pygame.draw.line(
                screen,
                (0,0,0),
                (br[0] + offset, br[1] - math.sqrt(3)*offset),
                (tl[0] + 2*offset, tl[1]),
            )

        shape = self.shape()
        for x in range(shape[0]):
            for y in range(shape[1]):
                for r in range(2):
                    self.grid[x, y, r].render(screen, self.grid_to_screen_coord(x, y, r))
