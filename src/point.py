import graphics


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
        if self.x % graphics.TILE_SIZE != 0 or self.y % graphics.TILE_SIZE != 0:
            raise ValueError("pixel point is on the tile grid")
        else:
            return TilePoint(int(self.x / graphics.TILE_SIZE),
                             int(self.y / graphics.TILE_SIZE))


class TilePoint(Point):
    def __init__(self, x: int, y: int):
        Point.__init__(self, x, y)

    def to_pixel_point(self) -> PixelPoint:
        return PixelPoint(self.x * graphics.TILE_SIZE,
                          self.y * graphics.TILE_SIZE)
