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

from yapsy.IPlugin import IPlugin

import colors
import players
import sprites
from classproperty import classproperty
from importer import Importer  # pylint: disable=no-name-in-module


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
    _name = NotImplemented  # type: str
    _code_name = NotImplemented  # type: str
    _sprite_location = ""  # type: str
    _initialized = False
    animation_speed = None

    def __init__(self):
        self._initialize_class_if_uninitialized()

    @classproperty
    def name(self):
        """str: The front end name."""
        return self._name

    @classproperty
    def code_name(self):
        """str: The internal name."""
        return self._code_name

    @property
    def animation(self):
        """sprites.SpriteAnimation: The entity's animation on the map."""
        raise NotImplementedError

    @property
    def sprite(self):
        """pygame.Surface: The entity's current sprite of its animation."""
        return self.animation.sprite

    @property
    def sprite_location(self):
        """str: The relative path to the animation sheet."""
        return self._sprite_location

    def _initialize_class_if_uninitialized(self):
        if not self._initialized:
            self._initialize_class()
            self._initialized = True

    def _initialize_class(self):
        raise NotImplementedError


class UnownedEntity(Entity, abc.ABC):
    """An entity that doesn't belong to a player."""
    _animation = NotImplemented  # type: sprites.SpriteAnimation

    def __init__(self):
        Entity.__init__(self)

    @property
    def animation(self) -> sprites.SpriteAnimation:
        """sprites.SpriteAnimation: The entity's animation on the screen."""
        return self._animation

    def _initialize_class(self):
        self._animation = sprites.SpriteAnimation(self.sprite_location,
                                                  self.code_name,
                                                  self.animation_speed)


class OwnedEntity(Entity, abc.ABC):
    """An entity that belongs to a player."""
    _army = NotImplemented  # type: armies.Army
    _sprite_location_type = NotImplemented  # type: str
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
        """armies.Army: The army this belongs to."""
        return self._army

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


class Building(OwnedEntity):
    """A building entity."""
    _sprite_location_type = "/buildings/"

    def __init__(self, player: players.Player):
        OwnedEntity.__init__(self, player)


class Unit(OwnedEntity):
    """A unit entity."""
    _sprite_location_type = "/units/"

    def __init__(self, player: players.Player):
        OwnedEntity.__init__(self, player)


class NullEntity(Entity):
    """A non-existent filler entity."""
    _name = "NULL ENTITY"
    _code_name = "null_entity"

    def __init__(self):
        Entity.__init__(self)

    @property
    def animation(self):
        """Raises an exception. NullEntities should not be drawn."""
        raise sprites.DrawNullEntityException()

    def _initialize_class(self):
        pass


class Terrain(UnownedEntity):
    """A terrain entity."""
    _sprite_location = "assets/terrain/"
    _defense = NotImplemented  # type: int

    def __init__(self):
        UnownedEntity.__init__(self)


class EntityPlugin(IPlugin):
    """Empty class to specify a plugin is an entity plugin."""
    pass


class EntityImporter(Importer):
    """Importer for grabbing entities out of the army folder."""

    def __init__(self):
        Importer.__init__(self, ["../armies"], EntityPlugin)


class Grass(Terrain):
    """Grass terrain type."""
    _name = "Grass"
    _code_name = "grass"
    _defense = 1
    _initialized = False

    def __init__(self):
        Terrain.__init__(self)


TERRAIN_LIST = [Grass]
