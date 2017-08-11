import abc


class Layer(abc.ABC):
    name = NotImplemented  # type: str
    priority = NotImplemented  # type: int


class TerrainLayer(Layer):
    name = "terrain"
    priority = 1


class BuildingLayer(Layer):
    name = "building"
    priority = 2


class UnitLayer(Layer):
    name = "unit"
    priority = 3


class OverlayLayer(Layer):
    name = "overlay"
    priority = 4


class CursorLayer(Layer):
    name = "cursor"
    priority = 5
