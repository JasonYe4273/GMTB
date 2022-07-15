class Triangle:
	o: Object

	def __init__(self):
		self.o = Empty()

	def get_object(self) -> Object:
		return self.o

	def set_object(self, obj: Object) -> None:
		self.o = obj

	def is_empty(self) -> bool:
		return typeof(self.o) == Empty
class Direction:
	X = 0
	Y = 1
	R = 2

DIRECTIONS = [Direction.X, Direction.Y, Direction.R]

class Object:
	def __init__(x_loc: int, y_loc: int, rad: int):
        self.x_location = x_loc
        self.y_location = y_loc
        self.rad_location = rad

    def get_location():
        return (self.x_location, self.y_location, self.rad_location)

    def set_location(x_loc: int, y_loc: int, rad: int):
        self.x_location = x_loc
        self.y_location = y_loc
        self.rad_location = rad
    
    def move(d: Direction):
        self.rad_location = (r+1)%2
        if d==Direction.X:
            self.y_location +=1
        if d==Direction.Y:
            self.y_location -=1
        if d==Direction.R:
            if self.rad_location==1:
                self.x_location -=1
        if d=="E":
            if self.rad_location==0:
                self.x_location +=1


class Dice extends Object:
    def __init__(x_loc: int, y_loc: int, rad int, faces: dict):
        super().__init__(x_loc, y_loc, rad)
        self.num = orientation.length
        self.faces = faces
        self.current_face = orientation[0]
       	 

    def roll(d: Direction):
        if d==Direction.X:
            self.current_face = self.faces[self.current_face][0]    
        if d==Direction.Y:
            self.current_face = self.faces[self.current_face][1]
        if d==Direction.R:
            self.current_face = self.faces[self.current_face][2]
    


class Player extends Object:
    def __init__(x_loc: int, y_loc: int, rad: int):
        super().__init__(x_loc, y_loc, rad)
