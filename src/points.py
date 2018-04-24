# MIT License
# Copyright (c) 2018 Toren James Darby
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Point data types

This module holds point data types, which represent coordinates.
"""

import abc

import graphics


class Point(abc.ABC):
    """A generic coordinate ABC

    Holds the functionality of a coordinate. All coordinates can be read and written in pixels or in
    tiles.
    """

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def tile(self):
        """tuple(int, int): The x, y coordinates in tiles."""
        return self.tile_x, self.tile_y

    @property
    def tile_x(self):
        """int: The x coordinate in tiles."""
        if self._x % graphics.TILE_SIZE != 0:
            raise ValueError("pixel point is not on the tile grid.")
        x = int(self._x / graphics.TILE_SIZE)
        return x

    @property
    def tile_y(self) -> int:
        """int: The y coordinate in tiles."""
        if self._y % graphics.TILE_SIZE != 0:
            raise ValueError("pixel point is not on the tile grid.")
        y = int(self._y / graphics.TILE_SIZE)
        return y

    @property
    def pixel(self) -> tuple:
        """Gets the pixel coordinates."""
        return self._x, self._y

    @property
    def pixel_x(self) -> int:
        """Gets the pixel x coordinate."""
        return self._x

    @property
    def pixel_y(self) -> int:
        """Gets the pixel y coordinate."""
        return self._y

    def directed_neighbour(self, direction):
        """Returns this point's neighbouring point in the given direction.

        This generates a new set of coordinates. It does not check that those coordinates point
        to anything, or are within any area.

        Args:
            direction (directions.Direction): The direction in which to generate the neighbour.

        Returns:
            Point: The generated point.
        """
        starting_point = MapPoint(self.pixel_x, self.pixel_y)
        return starting_point + direction.point

    @abc.abstractmethod
    def __str__(self):
        return

    def __add__(self, other):
        """Adds other point's x and y value to own x and y value."""
        return self.__class__(self.pixel_x + other.pixel_x, self.pixel_y + other.pixel_y)

    def __sub__(self, other):
        """Subtracts other point's x and y value from own x and y value."""
        return self.__class__(self.pixel_x - other.pixel_x, self.pixel_y - other.pixel_y)


class ScreenPoint(Point):
    """Coordinate on the screen"""

    def __init__(self, x, y):
        Point.__init__(self, x, y)

    def __str__(self):
        return "{}, {}".format(self.pixel_x, self.pixel_y)


class MapPoint(Point):
    """Coordinate on the map"""

    def __init__(self, x, y):
        Point.__init__(self, x, y)

    def __str__(self):
        return "{}, {}".format(self.tile_x, self.tile_y)


def point_from_tile(cls, x, y):
    """Generates a Point from given tile coordinates.

    Args:
        cls (Type[Point]): The point class to create.
        x (int): The x coordinate in tiles.
        y (int): The y coordinate in tiles.

    Returns:
        cls: The generated point.
    """
    return cls(graphics.TILE_SIZE * x, graphics.TILE_SIZE * y)
