import abc
import colors
import sprites
import pygame
from player import Player
from army import Army


class Entity(abc.ABC):
    _name = NotImplemented  # type: str
    _code_name = NotImplemented  # type: str
    _sprite_location = ""  # type: str
    _initialized = False

    def __init__(self):
        self._initialize_class_if_uninitialized()

    def get_name(self) -> str:
        return self._name

    def get_code_name(self) -> str:
        return self._code_name

    def get_animation(self) -> sprites.SpriteAnimation:
        raise NotImplementedError

    def get_sprite(self) -> pygame.Surface:
        return self.get_animation().get_sprite()

    def _get_sprite_location(self) -> str:
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

    def get_animation(self) -> sprites.SpriteAnimation:
        return self._animation

    def _initialize_class(self):
        self._animation = sprites.SpriteAnimation(self._get_sprite_location(),
                                                  self.get_code_name())


class OwnedEntity(Entity, abc.ABC):
    _army = NotImplemented  # type: Army
    _sprite_location_type = NotImplemented  # type: str
    _sprite_location = NotImplemented  # type: str
    _animation_red = NotImplemented  # type: sprites.SpriteAnimation
    _animation_blue = NotImplemented  # type: sprites.SpriteAnimation

    def __init__(self, player: Player, army: Army):
        self.player = player
        self.army = army
        Entity.__init__(self)

    def _initialize_class(self):
        self._army = self.army

        self._sprite_location = "armies/" + self.get_army().get_code_name() + "/sprites" + \
                                self._sprite_location_type

        self.__class__._animation_red = sprites.SpriteAnimation(self._get_sprite_location(),
                                                                self.get_code_name())
        self.__class__._animation_blue = sprites.SpriteAnimation(self._get_sprite_location(),
                                                                 self.get_code_name())

    def get_animation(self):
        color = self.player.get_color()
        if color == colors.Red:
            return self._animation_red
        elif color == colors.Blue:
            return self._animation_blue
        else:
            raise ValueError

    def get_army(self):
        return self._army


class Building(OwnedEntity):
    _sprite_location_type = "/buildings/"

    def __init__(self, player: Player, army: Army):
        OwnedEntity.__init__(self, player, army)


class Unit(OwnedEntity):
    _sprite_location_type = "/units/"

    def __init__(self, player: Player, army: Army):
        OwnedEntity.__init__(self, player, army)


class NullEntity(Entity):
    _name = "NULL ENTITY"
    _code_name = "null_entity"

    def __init__(self):
        Entity.__init__(self)

    def get_animation(self) -> sprites.SpriteAnimation:
        return None #fixme null animation with no sprites?

    def _initialize_class(self):
        pass

