import pygame
import math
from typing import List, Tuple, Optional

from images import *
from styles import *

class Direction:
    X = 0
    Y = 1
    R = 2

DIRECTIONS = [Direction.X, Direction.Y, Direction.R]

class Object:
    x: int
    y: int
    r: int
    
    def __init__(self, x_loc: int, y_loc: int, rad: int):
        self.x = x_loc
        self.y = y_loc
        self.r = rad

    def get_location(self) -> Tuple[int, int, int]:
        return (self.x, self.y, self.r)

    def set_location(self, x_loc: int, y_loc: int, rad: int) -> None:
        self.x = x_loc
        self.y = y_loc
        self.r = rad
    
    def move(self, d: Direction) -> None:
        self.r = (self.r + 1) % 2
        if d == Direction.X:
            if self.r == 0:
                self.x += 1
            else:
                self.x -= 1
        if d == Direction.Y:
            if self.r == 0:
                self.y += 1
            else:
                self.y -= 1

    def reset_value(self) -> None:
        pass

    def calc_value(self, input_num: Optional[int]=None) -> Optional[int]:
        return None

    def render(self, screen: pygame.Surface, left_corner: Tuple[float, float], unit: float) -> None:
        pass

    def render_static_image(self, screen: pygame.Surface, left_corner: Tuple[float, float], unit: float, image: pygame.Surface) -> None:
        # Scale the image
        scaled_img = pygame.transform.scale(image, (2*unit, math.sqrt(3)*unit))
        if self.r == 0:
            # If r=0, adjust the placement
            screen.blit(scaled_img, (left_corner[0], left_corner[1] - math.sqrt(3)*unit))
        else:
            # If r=1, flip the image
            flipped_img = pygame.transform.rotate(scaled_img, 180)
            screen.blit(flipped_img, left_corner)



class Empty(Object):
    def __init__(self, x_loc: int, y_loc: int, rad: int):
        super().__init__(x_loc, y_loc, rad)


class Wall(Object):
    def __init__(self, x_loc: int, y_loc: int, rad: int):
        super().__init__(x_loc, y_loc, rad)

    def render(self, screen: pygame.Surface, left_corner: Tuple[float, float], unit: float) -> None:
        self.render_static_image(screen, left_corner, unit, WALL_IMG)


class Dice(Object):
    current_face: str
    faces: dict
    value: Optional[int]
    valid: Optional[bool]

    def __init__(self, x_loc: int, y_loc: int, rad: int, faces: List[str]):
        super().__init__(x_loc, y_loc, rad)
        
        # Parse faces list
        # List of faces will be provided in the order [T, X, Y, R]
        self.current_face = faces[0]
        self.faces = dict()
        # When T is up, the order is [T, X, Y, R]
        self.faces[faces[0]] = [faces[1], faces[2], faces[3]]
        # When X is up, the order is [X, T, R, Y]
        self.faces[faces[1]] = [faces[0], faces[3], faces[2]]
        # When Y is up, the order is [Y, R, T, X]
        self.faces[faces[2]] = [faces[3], faces[0], faces[1]]
        # When R is up, the order is [R, Y, X, T]
        self.faces[faces[3]] = [faces[2], faces[1], faces[0]]

        self.value = None
        self.valid = None


    def move(self, d: Direction) -> None:
        super().move(d)
        self.current_face = self.faces[self.current_face][d]

    def reset_value(self) -> None:
        self.value = None
        self.valid = None

    def _set_value(self, value: int) -> None:
        if self.valid == False:
            return

        if self.value is None:
            self.value = value
            self.valid = True
        elif self.value != value:
            self.value = None
            self.valid = False

    def calc_value(self, input_num: Optional[int]=None) -> Optional[int]:
        if self.current_face.startswith('='):
            if input_num == int(self.current_face[1:]):
                self._set_value(input_num)
            elif input_num is not None:
                self.valid = False
        elif self.current_face.startswith('+'):
            if input_num is not None:
                self._set_value(input_num + int(self.current_face[1:]))
        elif self.current_face.startswith('-'):
            if input_num is not None:
                self._set_value(input_num - int(self.current_face[1:]))
        elif self.current_face.startswith('x'):
            if input_num is not None:
                self._set_value(input_num * int(self.current_face[1:]))
        elif self.current_face.startswith('/'):
            if input_num:
                self._set_value(input_num // int(self.current_face[1:]))
        else:
            self._set_value(int(self.current_face))

        return self.value

    def render(self, screen: pygame.Surface, left_corner: Tuple[float, float], unit: float) -> None:
        pygame.font.init()

        main_font = pygame.font.SysFont('Comic Sans MS', int(unit/3))
        xyr_font = pygame.font.SysFont('Comic Sans MS', int(unit/4))

        # Render text for die faces
        text_surface_1 = main_font.render(self.current_face, False, PURPLE)
        text_surface_x = xyr_font.render(self.faces[self.current_face][Direction.X], False, LIGHT_BLUE)
        text_surface_y = xyr_font.render(self.faces[self.current_face][Direction.Y], False, LIGHT_BLUE)
        text_surface_r = xyr_font.render(self.faces[self.current_face][Direction.R], False, LIGHT_BLUE)

        # Render text for calculated values
        text_surface_v = None
        if self.valid == False:
            text_surface_v = xyr_font.render('E', False, RED)
        elif self.value is not None:
            text_surface_v = xyr_font.render(str(self.value), False, GREEN)

        img = D4_IMG.copy()
        img.blit(text_surface_1, (img.get_width()/2, img.get_height()/2))
        img.blit(text_surface_x, (img.get_width()*3/4, img.get_height()*3/4))
        img.blit(text_surface_y, (img.get_width()*19/48, img.get_height()/5))
        img.blit(text_surface_r, (img.get_width()/8, img.get_height()*29/32))
        if text_surface_v:
            img.blit(text_surface_v, (img.get_width()*19/48, img.get_height()/2))

        self.render_static_image(screen, left_corner, unit, img)

class Player(Object):
    def __init__(self, x_loc: int, y_loc: int, rad: int):
        super().__init__(x_loc, y_loc, rad)

    def render(self, screen: pygame.Surface, left_corner: Tuple[float, float], unit: float) -> None:
        if self.r == 0:
            self.render_static_image(screen, left_corner, unit, PLAYER_IMG_0)
        else:
            self.render_static_image(screen, left_corner, unit, PLAYER_IMG_1)
