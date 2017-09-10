import abc

import points


class Direction(abc.ABC):
    def __init__(self, point: "points.Point"):
        self.point = point
        self.opposite = NotImplemented  # Must be set after creation :(


LEFT = Direction(points.Point.from_tile(-1, 0))
RIGHT = Direction(points.Point.from_tile(1, 0))
LEFT.opposite = RIGHT
RIGHT.opposite = LEFT

UP = Direction(points.Point.from_tile(0, -1))
DOWN = Direction(points.Point.from_tile(0, 1))
UP.opposite = DOWN
DOWN.opposite = UP

DIRECTIONS = [LEFT, RIGHT, UP, DOWN]
