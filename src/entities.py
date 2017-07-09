import pygame
import sprites
import abc


class Entity(abc.ABC):
    def __init__(self):
        self.animation = NotImplemented  # type: sprites.SpriteAnimation

    def get_sprite(self):
        return self.animation.get_sprite()

class Terrain(Entity):
    def __init__(self):
        Entity.__init__(self)


class Building(Entity):
    def __init__(self):
        Entity.__init__(self)


class Unit(Entity):
    def __init__(self):
        Entity.__init__(self)


class Grass(Terrain):
    def __init__(self):
        Terrain.__init__(self)
        self.name = "Grass"
        self.defense = 1
        self.animation = sprites.SpriteAnimation("grass.png")


class NullEntity(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.name = "NULL ENTITY"
