import pygame
import math

from images import PLAYER_IMG_0, PLAYER_IMG_1, WALL_IMG

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
        self.r = (self.r+1)%2
        if d==Direction.X:
            if self.r==0:
                self.x +=1
            else:
                self.x -= 1
        if d==Direction.Y:
            if self.r==0:
                self.y -= 1
            else:
                self.y +=1

    def render(self, screen: pygame.Surface, left_corner: tuple[float, float], unit: float) -> None:
        pass

    def render_static_image(self, screen: pygame.Surface, left_corner: tuple[float, float], unit: float, image: pygame.Surface) -> None:
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

    def render(self, screen: pygame.Surface, left_corner: tuple[float, float], unit: float) -> None:
        self.render_static_image(screen, left_corner, unit, WALL_IMG)


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

    def render(self, screen: pygame.Surface, left_corner: tuple[float, float], unit: float) -> None:
        self.render_static_image(screen, left_corner, unit, WALL_IMG)
    


class Player(Object):
    def __init__(self, x_loc: int, y_loc: int, rad: int):
        super().__init__(x_loc, y_loc, rad)

    def render(self, screen: pygame.Surface, left_corner: tuple[float, float], unit: float) -> None:
        if self.r == 0:
            self.render_static_image(screen, left_corner, unit, PLAYER_IMG_0)
        else:
            self.render_static_image(screen, left_corner, unit, PLAYER_IMG_1)
