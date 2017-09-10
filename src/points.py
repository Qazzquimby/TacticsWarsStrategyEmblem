import abc

import graphics


class Point(abc.ABC):
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @classmethod
    def from_tile(cls, x: int, y: int):
        return cls(graphics.TILE_SIZE * x, graphics.TILE_SIZE * y)

    @property
    def tile(self) -> tuple:
        """Gets the coordinates in 32x32px tiles"""
        if self._x % graphics.TILE_SIZE != 0 or self._y % graphics.TILE_SIZE != 0:
            raise ValueError("pixel point is not on the tile grid")
        else:
            return int(self._x / graphics.TILE_SIZE), int(self._y / graphics.TILE_SIZE)

    @property
    def tile_x(self) -> int:
        tile = self.tile
        return tile[0]

    @property
    def tile_y(self) -> int:
        tile = self.tile
        return tile[1]

    @property
    def pixel(self) -> tuple:
        """Gets the pixel coordinates"""
        return self._x, self._y

    @property
    def pixel_x(self) -> int:
        pixel = self.pixel
        return pixel[0]

    @property
    def pixel_y(self) -> int:
        pixel = self.pixel
        return pixel[1]

    @property
    def pixel_y(self) -> int:
        pixel = self.pixel
        return pixel[1]

    def directed_neighbour(self, direction):
        starting_point = Point(self.pixel_x, self.pixel_y)
        return starting_point + direction.point

    def __add__(self, other):
        return Point(self.pixel_x + other.pixel_x, self.pixel_y + other.pixel_y)


class ScreenPoint(Point):
    """Coordinate on the screen"""

    def __init__(self, x: int, y: int):
        Point.__init__(self, x, y)

    @classmethod
    def from_tile(cls, x: int, y: int) -> "ScreenPoint":
        return Point.from_tile(x, y)


class MapPoint(Point):
    """Coordinate on the map"""

    def __init__(self, x: int, y: int):
        Point.__init__(self, x, y)

    @classmethod
    def from_tile(cls, x: int, y: int) -> "MapPoint":
        return Point.from_tile(x, y)
