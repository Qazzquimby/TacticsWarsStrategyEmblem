import size_constants


class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Location(Point):
    def __init__(self, x: int, y: int):
        Point.__init__(self, x, y)


class PixelPoint(Point):
    def __init__(self, x: int, y: int):
        Point.__init__(self, x, y)

    def to_tile_point(self) -> "TilePoint":
        if self.x % size_constants.TILE_SIZE != 0 or self.y % size_constants.TILE_SIZE != 0:
            raise ValueError("pixel point is on the tile grid")
        else:
            return TilePoint(int(self.x / size_constants.TILE_SIZE),
                             int(self.y / size_constants.TILE_SIZE))


class TilePoint(Point):
    def __init__(self, x: int, y: int):
        Point.__init__(self, x, y)

    def to_pixel_point(self) -> PixelPoint:
        return PixelPoint(self.x * size_constants.TILE_SIZE,
                          self.y * size_constants.TILE_SIZE)
