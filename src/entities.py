# MIT License
# Copyright (c) 2018 Toren James Darby
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Classes related to entities."""

import abc
import typing

from yapsy.IPlugin import IPlugin

import colors
import players
import sprites
from importer import Importer  # pylint: disable=no-name-in-module

if typing.TYPE_CHECKING:
    # pylint: disable=unused-import
    import armies



class Entity(abc.ABC):
    """ABC for all entities.

    Attributes:
        self._name (str): The front end name.
        self._code_name (str): The internal name.
        self._sprite_location (str): The relative path to the sprite sheet.
        self._initialized (bool): If the class has received first time setup.
        self.animation_speed (Optional[int]): The length of each frame in the animation, or none for
        default.
    """
    _initialized = False
    animation_speed = None

    def __init__(self):
        self._initialize_class_if_uninitialized()

    @property
    @abc.abstractmethod
    def name(self):
        """str: The front end name."""
        return

    @property
    @abc.abstractmethod
    def code_name(self):
        """str: The internal name."""
        return

    @property
    @abc.abstractmethod
    def animation(self):
        """sprites.SpriteAnimation: The entity's animation on the map."""
        return

    @property
    def sprite(self):
        """pygame.Surface: The entity's current sprite of its animation."""
        return self.animation.sprite

    @property
    @abc.abstractmethod
    def sprite_location(self):
        """str: The relative path to the animation sheet."""
        return

    @property
    def is_null(self):
        """Returns that this is not a null entity.
        Overwritten by null_entity."""
        return False

    def _initialize_class_if_uninitialized(self):
        if not self._initialized:
            self._initialize_class()
            self._initialized = True

    @abc.abstractmethod
    def _initialize_class(self):
        return

    def __str__(self):
        return self.code_name


# noinspection PyAbstractClass
class UnownedEntity(Entity, abc.ABC):
    """An entity that doesn't belong to a player."""
    _sprite_location = NotImplemented
    _animation = NotImplemented

    def __init__(self):
        Entity.__init__(self)

    @property
    def animation(self):
        """sprites.SpriteAnimation: The entity's animation on the screen."""
        return self._animation

    @property
    def sprite_location(self):
        """str: Relative path the the entity's sprite animation."""
        return self._sprite_location

    def _initialize_class(self):
        self._animation = sprites.SpriteAnimation(self.sprite_location,
                                                  self.code_name,
                                                  self.animation_speed)


# noinspection PyAbstractClass
class OwnedEntity(Entity, abc.ABC):
    """An entity that belongs to a player."""
    _army = NotImplemented  # type: typing.Type[armies.Army]
    _sprite_location = NotImplemented  # type: str
    _animation_red = NotImplemented  # type: sprites.SpriteAnimation
    _animation_blue = NotImplemented  # type: sprites.SpriteAnimation

    def __init__(self, player: players.Player):
        self.player = player
        Entity.__init__(self)

    @property
    def animation(self):
        """sprites.SpriteAnimation: The animation in the entity's player's color."""
        color = self.player.color
        if color == colors.RED:
            return self._animation_red
        elif color == colors.BLUE:
            return self._animation_blue
        else:
            raise ValueError

    @property
    def army(self):
        """Type[armies.Army]: The army this belongs to."""
        return self._army

    @property
    def sprite_location(self):
        """str: Relative path to this entity's sprite animation."""
        return self._sprite_location

    @property
    def _sprite_location_type(self) -> str:
        return self._sprite_location

    def _initialize_class(self):
        self._army = self.army

        army_class = self.army
        army_instance = army_class()
        army_name = army_instance.code_name

        self._sprite_location = "army_plugins/{0}/sprites{1}".format(army_name,
                                                                     self._sprite_location_type)

        self._animation_red = sprites.SpriteAnimation(self.sprite_location,
                                                      self.code_name,
                                                      self.animation_speed)
        self._animation_blue = sprites.SpriteAnimation(self.sprite_location,
                                                       self.code_name,
                                                       self.animation_speed)
        self._army().add_entity(self.__class__)


# noinspection PyAbstractClass
class Building(OwnedEntity, abc.ABC):
    """A building entity."""

    def __init__(self, player: players.Player):
        OwnedEntity.__init__(self, player)

    @property
    def _sprite_location_type(self):
        return "/buildings/"


# noinspection PyAbstractClass
class Unit(OwnedEntity):
    """A unit entity."""
    _sprite_location_type = "/units/"

    def __init__(self, player: players.Player):
        OwnedEntity.__init__(self, player)


class NullEntity(Entity):
    """A non-existent filler entity."""

    def __init__(self):
        Entity.__init__(self)

    @property
    def name(self):
        """str: Outwards facing name."""
        return "NULL ENTITY"

    @property
    def code_name(self):
        """str: Debug name."""
        return "null_entity"

    @property
    def animation(self):
        """Raises an exception. NullEntities should not be drawn."""
        raise sprites.DrawNullEntityException()

    @property
    def sprite_location(self):
        """str: Filler function. Trying to draw the null entity results in an exception."""
        return ""

    @property
    def is_null(self):
        """bool: Returns that this is a null entity"""
        return True

    def _initialize_class(self):
        pass


class Terrain(UnownedEntity):
    """A terrain entity."""
    _sprite_location = "assets/terrain/"

    def __init__(self):
        UnownedEntity.__init__(self)

    @property
    @abc.abstractmethod
    def defense(self) -> int:
        """int: (Abstract) The defense transferred to a unit standing on this terrain."""
        pass


class EntityPlugin(IPlugin):
    """Empty class to specify a plugin is an entity plugin."""
    pass


class EntityImporter(Importer):
    """Importer for grabbing entities out of the army folder."""

    def __init__(self):
        Importer.__init__(self, ["../armies"], EntityPlugin)


class Grass(Terrain):
    """Grass terrain type."""
    _initialized = False

    def __init__(self):
        Terrain.__init__(self)

    @property
    def name(self):
        """str: Outwards facing name."""
        return "Grass"

    @property
    def code_name(self):
        """str: Inwards debug name."""
        return "grass"

    @property
    def defense(self):
        """int: Defense score added to units on this terrain."""
        return 1


TERRAIN_LIST = [Grass]
