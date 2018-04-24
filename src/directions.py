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

"""Simple direction management. Enumeration plus the direction's opposite."""


import abc

import points


class Direction(abc.ABC):
    """A direction on a grid.

    Attributes:
        self.point (points.Point): A point representing the direction. A given point plus
        this is translated one space in the direction.
        self.opposite (Direction): The Direction facing the opposite way (e.g. right -> left).
    """

    def __init__(self, point):
        self.point = point
        self.opposite = NotImplemented  # Must be set after creation :(


LEFT = Direction(points.point_from_tile(points.MapPoint, -1, 0))
RIGHT = Direction(points.point_from_tile(points.MapPoint, 1, 0))
LEFT.opposite = RIGHT
RIGHT.opposite = LEFT

UP = Direction(points.point_from_tile(points.MapPoint, 0, -1))
DOWN = Direction(points.point_from_tile(points.MapPoint, 0, 1))
UP.opposite = DOWN
DOWN.opposite = UP

DIRECTIONS = [LEFT, RIGHT, UP, DOWN]
