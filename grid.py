import numpy
from game_object import Triangle, Object, Empty, Direction
DIRECTIONS = [Direction.X, Direction.Y, Direction.R]

class Grid:
	def __init__(self, width: int, height: int):
		self.grid = numpy.full((width, height, 2), Triangle(), dtype=Triangle)

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

	def _add_dir(x: int, y: int, r: int, d: int) -> tuple[int, int, int]:
		if d == Direction.R:
			return (x, y, 1-r)

		pm = 1 if r == 1 else -1
		if d == Direction.X:
			return (x+pm, y, 1-r)
		if d == Direction.Y:
			return (x, y+pm, 1-r)

	def grid_get(self, x: int, y: int, r: int) -> Optional[Object]:
		_verify_coord(x, y, r)
		return self.grid[x][y][r].get_object(o)

	def grid_set(self, o: Object, x: int, y: int, r: int) -> None:
		_verify_coord(x, y, r)
		self.grid[x][y][r].set_object(o)

	def grid_adj(self, x: int, y: int, r: int) -> set(Direction):
		_verify_coord(x, y, r)
		adj: set[Direction] = set()

		for d in DIRECTIONS:
			(x2, y2, r2) = _add_dir(x, y, r, d)
			if _verify_coord(x2, y2, r2, False):
				adj.add(d)
		return adj

	def grid_move(self, x: int, y: int, r: int, d: int) -> None:
		_verify_coord(x,y,r)
		o = self.grid[x][y][r].get_object()

		(x2, y2, r2) = _add_dir(x, y, r, d)
		_verify_coord(x2, y2, r2)

		if not _self.grid[x2][y2][r2].is_empty():
			raise Exception(f"Cannot move from ({x}, {y}, {r}) into nonempty space at ({x2}, {y2}, {r2})")

		o.move(d, r)
		self.grid[x2][y2][r2].set_object(o)
		self.grid[x][y][r].set_object(Empty())
