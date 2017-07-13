import abc

import colors
import sprites


class Entity(abc.ABC):
    _name = NotImplemented
    _code_name = NotImplemented
    _sprite_location = ""
    _initialized = False

    def __init__(self):
        self._initialize_class_if_uninitialized()

    def _initialize_class_if_uninitialized(self):
        if not self._initialized:
            self._initialize_class()
            self._initialized = True

    def _initialize_class(self):
        raise NotImplementedError

    def get_name(self):
        return self._name

    def get_code_name(self):
        return self._code_name

    def _get_sprite_location(self):
        return self._sprite_location

    def get_animation(self):
        raise NotImplementedError

    def get_sprite(self):
        return self.get_animation().get_sprite()


class UnownedEntity(Entity):
    _animation = NotImplemented  # type: sprites.SpriteAnimation

    def __init__(self):
        Entity.__init__(self)

    def get_animation(self):
        return self.__class__._animation


class OwnedEntity(Entity):
    _army = NotImplemented  # type:army.Army
    _sprite_location_type = NotImplemented
    _sprite_location = NotImplemented
    _animation_red = NotImplemented
    _animation_blue = NotImplemented

    def __init__(self, player, army):
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

    def __init__(self, player, army):
        OwnedEntity.__init__(self, player, army)

        # def _initialize_class(self):


class Unit(OwnedEntity):
    _sprite_location_type = "/units/"

    def __init__(self, player, army):
        OwnedEntity.__init__(self, player, army)

    def _initialize_class(self):
        self.__class__._initialized = True
        self.__class__._animation = sprites.SpriteAnimation(self.__class__._sprite_location,
                                                            self.__class__._code_name)


class NullEntity(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.name = "NULL ENTITY"

    def _initialize_class(self):
        pass
