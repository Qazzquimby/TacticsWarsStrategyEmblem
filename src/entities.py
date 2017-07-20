import abc

import pygame
from yapsy.IPlugin import IPlugin

import colors
from classproperty import classproperty
import sprites
from importer import Importer
from player import Player


class Entity(abc.ABC):
    _name = NotImplemented  # type: str
    _code_name = NotImplemented  # type: str
    _sprite_location = ""  # type: str
    _initialized = False

    def __init__(self):
        self._initialize_class_if_uninitialized()

    @classproperty
    def name(self) -> str:
        return self._name

    @classproperty
    def code_name(self) -> str:
        return self._code_name

    @property
    def animation(self) -> sprites.SpriteAnimation:
        raise NotImplementedError

    @property
    def sprite(self) -> pygame.Surface:
        return self.animation.sprite

    @property
    def sprite_location(self) -> str:
        return self._sprite_location

    def _initialize_class_if_uninitialized(self):
        if not self._initialized:
            self._initialize_class()
            self._initialized = True

    def _initialize_class(self):
        raise NotImplementedError


class UnownedEntity(Entity, abc.ABC):
    _animation = NotImplemented  # type: sprites.SpriteAnimation

    def __init__(self):
        Entity.__init__(self)

    @property
    def animation(self) -> sprites.SpriteAnimation:
        return self._animation

    def _initialize_class(self):
        self._animation = sprites.SpriteAnimation(self.sprite_location,
                                                  self.code_name)


class OwnedEntity(Entity, abc.ABC):
    _army = NotImplemented  # type: armymod.Army
    _sprite_location_type = NotImplemented  # type: str
    _sprite_location = NotImplemented  # type: str
    _animation_red = NotImplemented  # type: sprites.SpriteAnimation
    _animation_blue = NotImplemented  # type: sprites.SpriteAnimation

    def __init__(self, player: Player):
        self.player = player
        Entity.__init__(self)

    def _initialize_class(self):
        self._army = self.army

        self._sprite_location = "armies/" + self.army().code_name + "/sprites" + \
                                self._sprite_location_type

        self._animation_red = sprites.SpriteAnimation(self.sprite_location,
                                                      self.code_name)
        self._animation_blue = sprites.SpriteAnimation(self.sprite_location,
                                                       self.code_name)
        self._army().add_entity(self.__class__)

    @property
    def animation(self):
        color = self.player.color
        if color == colors.Red:
            return self._animation_red
        elif color == colors.Blue:
            return self._animation_blue
        else:
            raise ValueError

    @property
    def army(self):
        return self._army


class Building(OwnedEntity):
    _sprite_location_type = "/buildings/"

    def __init__(self, player: Player):
        OwnedEntity.__init__(self, player)


class Unit(OwnedEntity):
    _sprite_location_type = "/units/"

    def __init__(self, player: Player):
        OwnedEntity.__init__(self, player)


class NullEntity(Entity):
    _name = "NULL ENTITY"
    _code_name = "null_entity"

    def __init__(self):
        Entity.__init__(self)

    @property
    def animation(self) -> sprites.SpriteAnimation:
        raise sprites.DrawNullEntityException()  # fixme null animation with no sprites?

    def _initialize_class(self):
        pass


class Terrain(UnownedEntity):
    _sprite_location = "sprites/terrain/"
    _defense = NotImplemented  # type: int

    def __init__(self):
        UnownedEntity.__init__(self)


class EntityPlugin(IPlugin):
    pass


class EntityImporter(Importer):
    def __init__(self):
        Importer.__init__(self, ["../armies"], EntityPlugin)


class Grass(Terrain):
    _name = "Grass"
    _code_name = "grass"
    _defense = 1
    _initialized = False

    def __init__(self):
        Terrain.__init__(self)


terrain_list = [Grass]
