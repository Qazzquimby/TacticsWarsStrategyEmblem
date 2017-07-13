import abc


class Layer(abc.ABC):
    priority = NotImplemented  # type: int


class TerrainLayer(Layer):
    priority = 1


class BuildingLayer(Layer):
    priority = 2


class UnitLayer(Layer):
    priority = 3


class OverlayLayer(Layer):
    priority = 4


class CursorLayer(Layer):
    priority = 5
