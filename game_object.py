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
    
    def move(self, d: int, front: bool, player_d: Optional[int]=None) -> None:
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

    def validate(self) -> bool:
        return True

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

class Dice(Object):
    current_face: str
    faces: dict
    value: Optional[int]
    valid: Optional[bool]

    def __init__(self, x_loc: int, y_loc: int, rad: int, faces: List[str]):
        super().__init__(x_loc, y_loc, rad)
        
        if rad == 0:
            # When faceup, list of faces provided in the order [T, Y, R, X]; need to reorder
            self.parse_face_list([faces[0], faces[3], faces[1], faces[2]])
        else:
            # When faceup, list of faces provided in the order [T, X, R, Y]; need to reorder
            self.parse_face_list([faces[0], faces[1], faces[3], faces[2]])

        self.value = None
        self.valid = None

    # Parse face list; should be provided in the order [T, X, Y, R]
    def parse_face_list(self, faces: List[str]) -> None:
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

    def move(self, d: int, front: bool, player_d: Optional[int]=None) -> None:
        super().move(d, front, player_d)
        if front and player_d is not None:
            t = self.current_face
            (x, y, r) = tuple(self.faces[self.current_face])
            if player_d == Direction.R:
                if d == Direction.X:
                    # [T, X, Y, R] -> [T, X, R, Y]
                    self.parse_face_list([t, y, r, x])
                elif d == Direction.Y:
                    # [T, X, Y, R] -> [T, Y, R, X]
                    self.parse_face_list([t, r, x, y])
            elif player_d == Direction.X:
                if d == Direction.Y:
                    # [T, X, Y, R] -> [T, R, X, Y]
                    self.parse_face_list([t, y, r, x])
                elif d == Direction.R:
                    # [T, X, Y, R] -> [T, Y, R, X]
                    self.parse_face_list([t, r, x, y])
            elif player_d == Direction.Y:
                if d == Direction.R:
                    # [T, X, Y, R] -> [T, Y, R, X]
                    self.parse_face_list([t, y, r, x])
                elif d == Direction.X:
                    # [T, X, Y, R] -> [T, R, X, Y]
                    self.parse_face_list([t, r, x, y])
        else:
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

    def validate(self) -> bool:
        return self.valid == True

    def render(self, screen: pygame.Surface, left_corner: Tuple[float, float], unit: float) -> None:
        pygame.font.init()

        main_font = pygame.font.SysFont('Comic Sans MS', int(unit*(3/4)))
        xyr_font = pygame.font.SysFont('Comic Sans MS', int(unit/2))

        # Render text for die faces

        text_surface_1 = main_font.render(self.current_face, False, PURPLE)
        text_surface_x = xyr_font.render(self.faces[self.current_face][Direction.X], False, LIGHT_BLUE)
        text_surface_y = xyr_font.render(self.faces[self.current_face][Direction.Y], False, LIGHT_BLUE)
        text_surface_r = xyr_font.render(self.faces[self.current_face][Direction.R], False, LIGHT_BLUE)
        
        if self.r == 1:
            text_surface_1 = pygame.transform.flip(text_surface_1, True, True)
            text_surface_y = pygame.transform.flip(text_surface_y, True, True)
            text_surface_r = pygame.transform.flip(text_surface_r, True, True)
            text_surface_x = pygame.transform.flip(text_surface_x, True, True)
        # Render text for calculated values
        text_surface_v = None
        if "=" in self.current_face:
            img = D4_BLUE_IMG.copy()
        elif "+" in self.current_face or "-" in self.current_face or "x" in self.current_face or "/" in self.current_face:
            img = D4_GREEN_IMG.copy()
        else:
            img = D4_RED_IMG.copy()
        
        if self.valid == False:
            pass
        elif self.value is not None:
            img = D4_YELLOW_IMG.copy()
        img.blit(text_surface_1, (img.get_width()*(1/2), img.get_height()*(5/12)))
        img.blit(text_surface_x, (img.get_width()*3/4, img.get_height()*(5/8)))
        img.blit(text_surface_y, (img.get_width()*19/48, img.get_height()/5))
        img.blit(text_surface_r, (img.get_width()*(3/16), img.get_height()*(13/16)))
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
