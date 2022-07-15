import numpy
from game_object import Object, Empty

class Grid:
	def __init__(self, width: int, height: int):
		self.grid = numpy.full((width, height, 2), Empty(), dtype=Object)

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

	def grid_get(self, x: int, y: int, r: int) -> Optional[Object]:
		_verify_coord(x, y, r)
		return self.grid[x][y][r]

	def grid_set(self, o: Object, x: int, y: int, r: int) -> None:
		_verify_coord(x, y, r)
		self.grid[x][y][r] = o

	def grid_adj(self, x: int, y: int, r: int) -> set(Object):
		_verify_coord(x, y, r)
		adj: set[Object] = set()

		if _verify_coord(x, y, 1-r, False):
			adj.add(self.grid[x][y][1-r])

		pm = 1 if r == 1 else -1
		if _verify_coord(x+pm, y, 1-r, False):
			adj.add(self.grid[x+pm][y][1-r])
		if _verify_coord(x, y+pm, 1-r, False):
			adj.add(self.grid[x][y+pm][1-r])

		return adj
