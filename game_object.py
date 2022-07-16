import pygame
import math

from images import WALL_IMG

class Direction:
    X = 0
    Y = 1
    R = 2

DIRECTIONS = [Direction.X, Direction.Y, Direction.R]

class Object:
    def __init__(self, x_loc: int, y_loc: int, rad: int):
        self.x = x_loc
        self.y = y_loc
        self.r = rad

    def get_location(self) -> None:
        return (self.x, self.y, self.r)

    def set_location(self, x_loc: int, y_loc: int, rad: int) -> None:
        self.x = x_loc
        self.y = y_loc
        self.r = rad
    
    def move(self, d: Direction) -> None:
        self.r = (r+1)%2
        if d==Direction.X:
            self.y +=1
        if d==Direction.Y:
            self.y -=1
        if d==Direction.R:
            if self.r==1:
                self.x -=1
        if d=="E":
            if self.r==0:
                self.x +=1

    def render(self, screen: pygame.Surface, left_corner: tuple[float, float], unit: float) -> None:
        print("Object")
        pass


class Empty(Object):
    def __init__(self, x_loc: int, y_loc: int, rad: int):
        super().__init__(x_loc, y_loc, rad)


class Wall(Object):
    def __init__(self, x_loc: int, y_loc: int, rad: int):
        super().__init__(x_loc, y_loc, rad)

    def render(self, screen: pygame.Surface, left_corner: tuple[float, float], unit: float) -> None:
        print(left_corner, self.x, self.y, self.r)
        scaled_img = pygame.transform.scale(WALL_IMG, (2*unit, math.sqrt(3)*unit))
        if self.r == 0:
            screen.blit(scaled_img, (left_corner[0], left_corner[1] - math.sqrt(3)*unit))
        else:
            flipped_img = pygame.transform.rotate(scaled_img, 180)
            screen.blit(flipped_img, left_corner)


class Dice(Object):
    def __init__(self, x_loc: int, y_loc: int, rad: int, faces: dict):
        super().__init__(x_loc, y_loc, rad)
        # self.num = orientation.length
        # self.faces = faces
        # self.current_face = orientation[0]
         

    def roll(d: Direction) -> None:
        if d==Direction.X:
            self.current_face = self.faces[self.current_face][0]    
        if d==Direction.Y:
            self.current_face = self.faces[self.current_face][1]
        if d==Direction.R:
            self.current_face = self.faces[self.current_face][2]
    


class Player(Object):
    def __init__(self, x_loc: int, y_loc: int, rad: int):
        super().__init__(x_loc, y_loc, rad)