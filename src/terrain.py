import sprites
from entities import UnownedEntity


class Terrain(UnownedEntity):
    _sprite_location = "sprites/terrain/"
    _defense = NotImplemented

    def __init__(self):
        UnownedEntity.__init__(self)

    def _initialize_class(self):
        self.__class__._initialized = True
        self.__class__._animation = sprites.SpriteAnimation(self.__class__._sprite_location,
                                                            self.__class__._code_name)


class Grass(Terrain):
    _name = "Grass"
    _code_name = "grass"
    _defense = 1
    _initialized = False

    def __init__(self):
        Terrain.__init__(self)
        self._initialize_class_if_uninitialized()


