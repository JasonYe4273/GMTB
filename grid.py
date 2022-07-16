import numpy
import math
import pygame
from game_object import Object, Empty
from styles import BLACK

class Direction:
    X = 0
    Y = 1
    R = 2

DIRECTIONS = [Direction.X, Direction.Y, Direction.R]


class Triangle:
    o: Object                           # object in the triangle
    x: int                              # x-coordinate in the grid
    y: int                              # y-coordinate in the grid
    r: int                              # r-coordinate in the grid
    screen: pygame.Surface              # pygame screen to render to
    left_corner: tuple[float, float]    # pixel corner for the left corner of the triangle
    unit: float                         # pixel length of half of a triangle side

    def __init__(self, x_loc: int, y_loc: int, rad: int, screen: pygame.Surface, left_corner: tuple[float, float], unit: float):
        self.o = Empty(x_loc, y_loc, rad)
        self.x = x_loc
        self.y = y_loc
        self.r = rad
        self.screen = screen
        self.left_corner = left_corner
        self.unit = unit

    # Get the object in this triangle
    def get_object(self) -> Object:
        return self.o

    # Set the object in this triangle
    def set_object(self, obj: Object) -> None:
        self.o = obj
        self.render()

    # Check if the triangle is empty
    def is_empty(self) -> bool:
        return typeof(self.o) == Empty

    # Render the triangle
    def render(self) -> None:
        self.o.render(self.screen, self.left_corner, self.unit)


class Grid:
    MARGIN: int = 200       # pixel margin on the screen
    grid: any               # array of triangles representing the grid
    unit: float             # unit length in pixels equal to half of a triangle side
    bl: tuple[float, float] # pixel coordinates for bottom left corner of the grid
    screen: pygame.Surface  # pygame screen to render to

    def __init__(self, width: int, height: int, screen: pygame.Surface):
        self.screen = screen
        self.grid = numpy.full((width, height, 2), None)

        (screen_w, screen_h) = screen.get_size()
        (adj_w, adj_h) = (screen_w - self.MARGIN, screen_h - self.MARGIN)
        x = 2*width + height
        y = math.sqrt(3)*height

        self.unit = min(adj_w / x, adj_h / y)
        grid_w = self.unit * x
        grid_h = self.unit * y

        self.bl = ((screen_w - grid_w) / 2, (screen_h + grid_h) / 2)

        for i in range(width):
            for j in range(height):
                for r in range(2):
                    self.grid[i, j, r] = Triangle(i, j, r, screen, self.grid_to_screen_coord(i, j, r), self.unit)

    # Verify that the coordinates are in the grid, and raise an exception if not
    def _verify_coord(self, x: int, y: int, r: int, raise_if_bad: bool=True) -> bool:
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

    # Get the coordinates shifted in that direction
    def _add_dir(self, x: int, y: int, r: int, d: int) -> tuple[int, int, int]:
        if d == Direction.R:
            return (x, y, 1-r)

        pm = 1 if r == 1 else -1
        if d == Direction.X:
            return (x+pm, y, 1-r)
        if d == Direction.Y:
            return (x, y+pm, 1-r)

    # Get the dimensions of the grid
    def shape(self) -> tuple[int, int]:
        return (self.grid.shape[0], self.grid.shape[1])

    # Get the triangle at the given coordinates
    def get_triangle(self, x: int, y: int, r: int) -> Object:
        self._verify_coord(x, y, r)
        return self.grid[x, y, r]

    # Get the object at the given coordinates
    def get_object(self, x: int, y: int, r: int) -> Object:
        self._verify_coord(x, y, r)
        return self.grid[x, y, r].get_object(o)

    # Set the object at the given coordinates
    def set_object(self, o: Object, x: int, y: int, r: int) -> None:
        self._verify_coord(x, y, r)
        self.grid[x, y, r].set_object(o)

    # Get the directions adjacent to the given coordinates
    def grid_adj(self, x: int, y: int, r: int) -> set[Direction]:
        self._verify_coord(x, y, r)
        adj: set[Direction] = set()

        for d in DIRECTIONS:
            (x2, y2, r2) = self._add_dir(x, y, r, d)
            if self._verify_coord(x2, y2, r2, False):
                adj.add(d)
        return adj

    # Move an object at the given coordinates in the given direction
    def move_object(self, x: int, y: int, r: int, d: int) -> None:
        self._verify_coord(x,y,r)
        o = self.grid[x, y, r].get_object()

        (x2, y2, r2) = self._add_dir(x, y, r, d)
        self._verify_coord(x2, y2, r2)

        if not _self.grid[x2, y2, r2].is_empty():
            raise Exception(f"Cannot move from ({x}, {y}, {r}) into nonempty space at ({x2}, {y2}, {r2})")

        o.move(d)
        self.grid[x2, y2, r2].set_object(o)
        self.grid[x, y, r].set_object(Empty())


    # Convert grid coordinates to pixel coordinates
    def grid_to_screen_coord(self, x: int, y: int, r: int) -> tuple[float, float]:
        rhombus_bl = (self.bl[0] + 2*x*self.unit + y*self.unit, self.bl[1] - math.sqrt(3)*y*self.unit)

        if r == 0:
            return rhombus_bl
        else:
            return (rhombus_bl[0] + self.unit, rhombus_bl[1] - math.sqrt(3)*self.unit)

    # Render the grid
    def render_all(self) -> None:
        (grid_x, grid_y) = self.shape()

        # Draw horizontals
        for j in range(grid_y+1):
            x_offset = 2*grid_x*self.unit
            y_offset = j*self.unit
            pygame.draw.line(
                self.screen,
                BLACK,
                (self.bl[0] + y_offset, self.bl[1] - math.sqrt(3)*y_offset),
                (self.bl[0] + y_offset + x_offset, self.bl[1] - math.sqrt(3)*y_offset)
            )

        # Draw long diagonals
        for i in range(grid_x+1):
            x_offset = 2*i*self.unit
            y_offset = grid_y*self.unit
            pygame.draw.line(
                self.screen,
                BLACK,
                (self.bl[0] + x_offset, self.bl[1]),
                (self.bl[0] + x_offset + y_offset, self.bl[1] - math.sqrt(3)*y_offset)
            )

        # Draw cross diagonals
        for i in range(grid_x):
            offset = i*self.unit
            pygame.draw.line(
                self.screen,
                BLACK,
                (self.bl[0] + 2*offset, self.bl[1]),
                (self.bl[0] + offset, self.bl[1] - math.sqrt(3)*offset),
            )
        for i in range(grid_y):
            br = (self.bl[0] + 2*grid_x*self.unit, self.bl[1])
            tl = (self.bl[0] + grid_y*self.unit, self.bl[1] - math.sqrt(3)*grid_y*self.unit)

            offset = i*self.unit
            pygame.draw.line(
                self.screen,
                BLACK,
                (br[0] + offset, br[1] - math.sqrt(3)*offset),
                (tl[0] + 2*offset, tl[1]),
            )

        # Render triangles
        shape = self.shape()
        for x in range(shape[0]):
            for y in range(shape[1]):
                for r in range(2):
                    self.grid[x, y, r].render()
