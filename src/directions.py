import abc

from classproperty import classproperty
from points import Point


class Direction(abc.ABC):
    point = NotImplemented

    @classproperty
    def opposite(self):
        return NotImplementedError


class Left(Direction):
    point = Point.from_tile(-1, 0)

    @classproperty
    def opposite(self):
        return Right


class Right(Direction):
    point = Point.from_tile(1, 0)

    @classproperty
    def opposite(self):
        return Left


class Up(Direction):
    point = Point.from_tile(0, -1)

    @classproperty
    def opposite(self):
        return Down


class Down(Direction):
    point = Point.from_tile(0, 1)

    @classproperty
    def opposite(self):
        return Up


DIRECTIONS = [Left, Right, Up, Down]
