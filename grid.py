import numpy
import math
import pygame
from game_object import *
from styles import *

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

    # Check if the triangle is empty
    def is_empty(self) -> bool:
        return type(self.o) == Empty

    # Check if the object in the triangle is pushable
    def is_pushable(self) -> bool:
        return type(self.o) == Dice

    # Render the triangle
    def render(self, color: tuple[int, int, int]) -> None:
        pm = 1 if self.r == 1 else -1
        margin = self.unit*0.05

        pygame.draw.polygon(
            self.screen,
            [*color, 0.3],
            [
                (self.left_corner[0] + math.sqrt(3)*margin, self.left_corner[1] + pm*margin),
                (self.left_corner[0] + 2*self.unit - math.sqrt(3)*margin, self.left_corner[1] + pm*margin),
                (self.left_corner[0] + self.unit, self.left_corner[1] + pm*math.sqrt(3)*self.unit - 2*pm*margin)
            ],
        )
        self.o.render(self.screen, self.left_corner, self.unit)


class Grid:
    MARGIN: int = 200                   # pixel margin on the screen

    grid: any                           # array of triangles representing the grid

    unit: float                         # unit length in pixels equal to half of a triangle side
    bl: tuple[float, float]             # pixel coordinates for bottom left corner of the grid
    screen: pygame.Surface              # pygame screen to render to

    player: Player                      # Player object

    def __init__(self, width: int, height: int, screen: pygame.Surface):
        self.screen = screen
        self.grid = numpy.full((width, height, 2), None)
        self.player = None

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
                raise Exception(f"x coordinate {x} out of bounds")
            return False
        if y < 0 or y >= self.grid.shape[1]:
            if raise_if_bad:
                raise Exception(f"y coordinate {y} out of bounds")
            return False
        if r < 0 or r > 1:
            if raise_if_bad:
                raise Exception(f"r coordinate {r} out of bounds")
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

        if not self.grid[x2, y2, r2].is_empty():
            raise Exception(f"Cannot move from ({x}, {y}, {r}) into nonempty space at ({x2}, {y2}, {r2})")
        e = self.grid[x2, y2, r2].get_object()

        e.move(d)
        self.grid[x, y, r].set_object(e)

        o.move(d)
        self.grid[x2, y2, r2].set_object(o)

    # Add objects from level JSON
    def add_objects(self, objects: any) -> None:
        for o in objects:
            (x, y, r) = o["loc"]
            if o["type"] == "start":
                self.player = Player(x, y, r)
                self.set_object(self.player, x, y, r)
            elif o["type"] == "d4":
                d4 = Dice(x, y, r, dict())
                self.set_object(d4, x, y, r)
            elif o["type"] == "wall":
                wall = Wall(x, y, r)
                self.set_object(wall, x, y, r)


    # Move player
    def move_player(self, d: int) -> None:
        if not self.player:
            return
        self.move_object(self.player.x, self.player.y, self.player.r, d)


    # Convert grid coordinates to pixel coordinates
    def grid_to_screen_coord(self, x: int, y: int, r: int) -> tuple[float, float]:
        rhombus_bl = (self.bl[0] + 2*x*self.unit + y*self.unit, self.bl[1] - math.sqrt(3)*y*self.unit)

        if r == 0:
            return rhombus_bl
        else:
            return (rhombus_bl[0] + self.unit, rhombus_bl[1] - math.sqrt(3)*self.unit)

    # Convert pixel coordinates to grid coordinates
    def screen_to_grid_coord(self, coordinates: tuple[float, float]) -> tuple[int, int, int]:
        # Find the grid coordinates of the mouse
        grid_y = (self.bl[1] - coordinates[1]) / (math.sqrt(3)*self.unit)
        grid_x = (coordinates[0] - self.bl[0] - grid_y*self.unit) / (2*self.unit)

        # Find the r coordinate by comparing it against the diagonal
        x = math.floor(grid_x)
        y = math.floor(grid_y)
        r = 0 if grid_x + grid_y < x + y + 1 else 1
        return (x, y, r)

    # Handle mouse click
    def handle_click(self, mouse_pos: tuple[float, float]) -> None:
        # Check that the mouse is in the grid
        clicked = self.screen_to_grid_coord(mouse_pos)
        if not self._verify_coord(*clicked, False):
            return

        # Check if click location is a valid move location
        if self.player:
            for d in self.grid_adj(self.player.x, self.player.y, self.player.r):
                # Find all adjacent triangles
                adj = self._add_dir(self.player.x, self.player.y, self.player.r, d)

                # Can move to empty triangles
                if clicked == adj and self.grid[adj].is_empty():
                    self.move_object(self.player.x, self.player.y, self.player.r, d)
                    return

                # Can maybe move to pushable triangles
                elif self.grid[adj].is_pushable():
                    # Check adjacent triangles to the triangle you're pushing
                    for adj_d in self.grid_adj(*adj):
                        adj_adj = self._add_dir(*adj, adj_d)
                        if adj_adj == (self.player.x, self.player.y, self.player.r):
                            continue

                        # Can only push to empty triangles
                        if clicked == adj_adj and self.grid[adj_adj].is_empty():
                            # First move pushable object
                            self.move_object(*adj, adj_d)
                            # Then move player
                            self.move_object(self.player.x, self.player.y, self.player.r, d)
                            return

    # Render the grid
    def render_all(self, mouse_pos: tuple[float, float]) -> None:
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
            diag_length = min(grid_y, i)
            back_offset = diag_length*self.unit

            pygame.draw.line(
                self.screen,
                BLACK,
                (self.bl[0] + 2*offset, self.bl[1]),
                (self.bl[0] + 2*offset - back_offset, self.bl[1] - math.sqrt(3)*back_offset),
            )
        for i in range(grid_y):
            br = (self.bl[0] + 2*grid_x*self.unit, self.bl[1])
            diag_length = min(grid_x, grid_y - i)
            back_offset = diag_length*self.unit

            offset = i*self.unit
            pygame.draw.line(
                self.screen,
                BLACK,
                (br[0] + offset, br[1] - math.sqrt(3)*offset),
                (br[0] + offset - back_offset, br[1] - math.sqrt(3)*offset - math.sqrt(3)*back_offset),
            )

        (mouse_x, mouse_y, mouse_r) = self.screen_to_grid_coord(mouse_pos)

        # Color grid based on player movement options
        color_grid = numpy.full([grid_x, grid_y, 2, 3], WHITE)
        if self.player:
            for d in self.grid_adj(self.player.x, self.player.y, self.player.r):
                # Find all adjacent triangles
                adj = self._add_dir(self.player.x, self.player.y, self.player.r, d)

                # Can move to empty triangles
                if self.grid[adj].is_empty():
                    color_grid[adj] = GREEN

                # Can maybe move to pushable triangles
                elif self.grid[adj].is_pushable():
                    # Check whether you're mousing over the pushabale triangle or any of its adjacent triangles
                    moused_over = adj == (mouse_x, mouse_y, mouse_r)
                    if not moused_over:
                        for adj_d in self.grid_adj(*adj):
                            adj_adj = self._add_dir(*adj, adj_d)
                            if adj_adj == (self.player.x, self.player.y, self.player.r):
                                continue
                                
                            if adj_adj == (mouse_x, mouse_y, mouse_r):
                                moused_over = True

                    # Check adjacent triangles to the triangle you're pushing
                    can_push = False
                    for adj_d in self.grid_adj(*adj):
                        adj_adj = self._add_dir(*adj, adj_d)
                        if adj_adj == (self.player.x, self.player.y, self.player.r):
                            continue

                        # Can only push to empty triangles
                        if self.grid[adj_adj].is_empty():
                            can_push = True
                            # Only color if moused over
                            if moused_over:
                                color_grid[adj_adj] = GREEN

                    # Blue if you can push and it's moused-over, otherwise green.
                    if can_push:
                        if moused_over:
                            color_grid[adj] = BLUE
                        else:
                            color_grid[adj] = GREEN

        # Render triangles
        shape = self.shape()
        for x in range(shape[0]):
            for y in range(shape[1]):
                for r in range(2):
                    # If mouseover, then turn the color lighter
                    color = tuple(color_grid[x, y, r])
                    if (x, y, r) == (mouse_x, mouse_y, mouse_r):
                        if color == GREEN:
                            color = LIGHT_GREEN
                        elif color == BLUE:
                            color = LIGHT_BLUE

                    self.grid[x, y, r].render(color)
