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
    
    def move(d: str):
        self.rad_location = (r+1)%2
        if d=="N":
            self.y_location +=1
        if d=="S":
            self.y_location -=1
        if d=="W":
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
       	 

    def roll(d: str):
        if d=="N":
            self.current_face = self.faces[self.current_face][1]    
        if d=="S":
            self.current_face = self.faces[self.current_face][0]
        if d=="EW":
            self.current_face = self.faces[self.current_face][2]
    


class Player extends Object:
    def __init__(x_loc: int, y_loc: int, rad: int):
        super().__init__(x_loc, y_loc, rad)
