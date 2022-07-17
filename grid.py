import numpy
import math
import pygame
from game_object import *
from styles import *
from typing import Tuple, Set, List, Optional

from images import *

class Direction:
    X = 0
    Y = 1
    R = 2

    @staticmethod
    def left(direction: int) -> int:
        return (direction + 2) % 3

    @staticmethod
    def right(direction: int) -> int:
        return (direction + 1) % 3

DIRECTIONS = [Direction.X, Direction.Y, Direction.R]


class Move:
    player_end: Tuple[int, int, int]
    player_dir: int
    dice_end: Optional[Tuple[int, int, int]]
    dice_dir: Optional[int]

    def __init__(self, p_end: Tuple[int, int, int], p_dir: int, d_end: Optional[Tuple[int, int, int]]=None, d_dir: Optional[int]=None):
        self.player_end = p_end
        self.player_dir = p_dir
        self.dice_end = d_end
        self.dice_dir = d_dir


class Triangle:
    o: Object                           # object in the triangle

    x: int                              # x-coordinate in the grid
    y: int                              # y-coordinate in the grid
    r: int                              # r-coordinate in the grid

    screen: pygame.Surface              # pygame screen to render to
    left_corner: Tuple[float, float]    # pixel corner for the left corner of the triangle
    unit: float                         # pixel length of half of a triangle side

    def __init__(self, x_loc: int, y_loc: int, rad: int, screen: pygame.Surface, left_corner: Tuple[float, float], unit: float):
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
    def render(self, arrow_direction: int, arrow_type: int, mouseover: bool) -> None:
        self.o.render(self.screen, self.left_corner, self.unit)

        # Determine arrow type
        img = None
        if arrow_type == 0:
            if mouseover:
                img = MOVE_ARROW_HOVER
            else:
                img = MOVE_ARROW
        elif arrow_type == 1:
            if mouseover:
                img = PUSH_ARROW_BOTH_HOVER
            else:
                img = PUSH_ARROW_BOTH
        elif arrow_type == 2:
            if mouseover:
                img = pygame.transform.flip(PUSH_ARROW_RIGHT_HOVER, True, False)
            else:
                img = pygame.transform.flip(PUSH_ARROW_RIGHT, True, False)
        elif arrow_type == 3:
            if mouseover:
                img = PUSH_ARROW_RIGHT_HOVER
            else:
                img = PUSH_ARROW_RIGHT

        if img:
            # Scale and rotate arrow image
            img = pygame.transform.scale(img, (self.unit, self.unit/2))
            rotation = 0
            if arrow_direction == Direction.Y:
                if self.r == 0:
                    rotation = 180
            elif arrow_direction == Direction.X:
                if self.r == 0:
                    rotation = 60
                else:
                    rotation = 240
            elif arrow_direction == Direction.R:
                if self.r == 0:
                    rotation = 300
                else:
                    rotation = 120

            if rotation > 0:
                img = pygame.transform.rotate(img, rotation)

            # Move the arrow to the right position
            x_offset = 0
            y_offset = 0

            # Don't question the math here it's hell
            if arrow_direction == Direction.Y:
                if self.r == 0:
                    x_offset = self.unit / 2
                    y_offset = -self.unit / 2
                else:
                    x_offset = self.unit / 2
            elif arrow_direction == Direction.X:
                if self.r == 0:
                    x_offset = self.unit / 4
                    y_offset = -self.unit * 3 * math.sqrt(3) / 4
                else:
                    x_offset = self.unit * (5 - math.sqrt(3)) / 4
                    y_offset = self.unit * (math.sqrt(3) - 1) / 4
            elif arrow_direction == Direction.R:
                if self.r == 0:
                    x_offset = self.unit * (5 - math.sqrt(3)) / 4
                    y_offset = -self.unit * 3 * math.sqrt(3) / 4
                else:
                    x_offset = self.unit / 4
                    y_offset = self.unit * (math.sqrt(3) - 1) / 4

            self.screen.blit(img, (self.left_corner[0] + x_offset, self.left_corner[1] + y_offset))



class Grid:
    MARGIN: int = 200                   # pixel margin on the screen

    grid: any                           # array of triangles representing the grid

    unit: float                         # unit length in pixels equal to half of a triangle side
    bl: Tuple[float, float]             # pixel coordinates for bottom left corner of the grid
    screen: pygame.Surface              # pygame screen to render to

    player: Player                      # Player object
    undo_stack: List[Move]              # Stack of moves for undo purposes

    def __init__(self, width: int, height: int, screen: pygame.Surface):
        self.screen = screen
        self.grid = numpy.full((width, height, 2), None)
        self.player = None
        self.undo_stack = []

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
    def _add_dir(self, x: int, y: int, r: int, d: int) -> Tuple[int, int, int]:
        if d == Direction.R:
            return (x, y, 1-r)

        pm = 1 if r == 1 else -1
        if d == Direction.X:
            return (x+pm, y, 1-r)
        if d == Direction.Y:
            return (x, y+pm, 1-r)

    # Get the dimensions of the grid
    def shape(self) -> Tuple[int, int]:
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
    def grid_adj(self, x: int, y: int, r: int) -> Set[Direction]:
        self._verify_coord(x, y, r)
        adj: Set[Direction] = set()

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
                d4 = Dice(x, y, r, o["faces"])
                self.set_object(d4, x, y, r)
            elif o["type"] == "wall":
                wall = Wall(x, y, r)
                self.set_object(wall, x, y, r)


    # Convert grid coordinates to pixel coordinates
    def grid_to_screen_coord(self, x: int, y: int, r: int) -> Tuple[float, float]:
        rhombus_bl = (self.bl[0] + 2*x*self.unit + y*self.unit, self.bl[1] - math.sqrt(3)*y*self.unit)

        if r == 0:
            return rhombus_bl
        else:
            return (rhombus_bl[0] + self.unit, rhombus_bl[1] - math.sqrt(3)*self.unit)

    # Convert pixel coordinates to grid coordinates
    def screen_to_grid_coord(self, coordinates: Tuple[float, float]) -> Tuple[int, int, int]:
        # Find the grid coordinates of the mouse
        grid_y = (self.bl[1] - coordinates[1]) / (math.sqrt(3)*self.unit)
        grid_x = (coordinates[0] - self.bl[0] - grid_y*self.unit) / (2*self.unit)

        # Find the r coordinate by comparing it against the diagonal
        x = math.floor(grid_x)
        y = math.floor(grid_y)
        r = 0 if grid_x + grid_y < x + y + 1 else 1
        return (x, y, r)

    # Handle mouse click
    def handle_click(self, mouse_pos: Tuple[float, float]) -> None:
        # Check that the mouse is in the grid
        clicked = self.screen_to_grid_coord(mouse_pos)
        if not self._verify_coord(*clicked, False):
            return

        # Check if click location is a valid move location
        player_location = self.player.get_location()
        if self.player:
            for d in self.grid_adj(*player_location):
                # Find all adjacent triangles
                adj = self._add_dir(*player_location, d)

                # Can move to empty triangles
                if clicked == adj and self.grid[adj].is_empty():
                    self.move_object(*player_location, d)
                    self.undo_stack.append(Move(adj, d))
                    return

                # Can maybe move to pushable triangles
                elif self.grid[adj].is_pushable():
                    # Check adjacent triangles to the triangle you're pushing
                    for adj_d in self.grid_adj(*adj):
                        adj_adj = self._add_dir(*adj, adj_d)
                        if adj_adj == player_location:
                            continue

                        # Can only push to empty triangles
                        if clicked == adj_adj and self.grid[adj_adj].is_empty():
                            # First move pushable object
                            self.move_object(*adj, adj_d)
                            # Then move player
                            self.move_object(*player_location, d)

                            self.undo_stack.append(Move(adj, d, adj_adj, adj_d))
                            return

    # Render the grid
    def render_all(self, mouse_pos: Tuple[float, float]) -> None:
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

        # Arrow grid based on player movement options: arrows are represented by (direction, type)
        arrow_grid = numpy.full([grid_x, grid_y, 2, 2], [-1, -1])
        if self.player:
            for d in self.grid_adj(*self.player.get_location()):
                # Find all adjacent triangles
                adj = self._add_dir(*self.player.get_location(), d)

                # Can move to empty triangles
                if self.grid[adj].is_empty():
                    arrow_grid[adj] = [d, 0]

                # Can maybe move to pushable triangles
                elif self.grid[adj].is_pushable():
                    # Check whether you're mousing over the pushabale triangle or any of its adjacent triangles
                    moused_over = adj == (mouse_x, mouse_y, mouse_r)
                    if not moused_over:
                        for adj_d in self.grid_adj(*adj):
                            adj_adj = self._add_dir(*adj, adj_d)
                            if adj_adj == self.player.get_location():
                                continue
                                
                            if adj_adj == (mouse_x, mouse_y, mouse_r):
                                moused_over = True

                    # Check adjacent triangles to the triangle you're pushing
                    can_push_left = False
                    left_dir = Direction.left(d)
                    adj_left = self._add_dir(*adj, left_dir)
                    if self._verify_coord(*adj_left, False) and self.grid[adj_left].is_empty():
                        can_push_left = True
                        if moused_over:
                            arrow_grid[adj_left] = [left_dir, 0]

                    can_push_right = False
                    right_dir = Direction.right(d)
                    adj_right = self._add_dir(*adj, right_dir)
                    if self._verify_coord(*adj_right, False) and self.grid[adj_right].is_empty():
                        can_push_right = True
                        if moused_over:
                            arrow_grid[adj_right] = [right_dir, 0]

                    # Blue if you can push.
                    if can_push_left and can_push_right:
                        arrow_grid[adj] = [d, 1]
                    elif can_push_left:
                        arrow_grid[adj] = [d, 2]
                    elif can_push_right:
                        arrow_grid[adj] = [d, 3]

        # Render triangles
        shape = self.shape()
        for x in range(shape[0]):
            for y in range(shape[1]):
                for r in range(2):
                    self.grid[x, y, r].render(*arrow_grid[x, y, r], (x, y, r) == (mouse_x, mouse_y, mouse_r))


    # Undo last move
    def undo(self):
        if len(self.undo_stack) > 0:
            m = self.undo_stack.pop()
            self.move_object(*m.player_end, m.player_dir)
            if m.dice_end:
                self.move_object(*m.dice_end, m.dice_dir)

    # Reset puzzle
    def reset(self):
        pass
