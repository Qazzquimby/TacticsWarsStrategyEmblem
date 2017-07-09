import size_constants


class Location(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class PixelPoint(Point):
    def __init__(self, x: int, y: int):
        Point.__init__(self, x, y)

    def to_tile_point(self):
        if self.x % size_constants.TILE_SIZE != 0 or self.y % size_constants.TILE_SIZE != 0:
            raise ValueError("pixel point is on the tile grid")
        else:
            return TilePoint(int(self.x/size_constants.TILE_SIZE),
                             int(self.y/size_constants.TILE_SIZE))


class TilePoint(Point):
    def __init__(self, x: int, y: int):
        Point.__init__(self, x, y)

    def to_pixel_point(self):
        return PixelPoint(self.x * size_constants.TILE_SIZE,
                          self.y * size_constants.TILE_SIZE)