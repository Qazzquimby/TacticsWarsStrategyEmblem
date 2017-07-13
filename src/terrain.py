from entities import UnownedEntity


class Terrain(UnownedEntity):
    _sprite_location = "sprites/terrain/"
    _defense = NotImplemented  # type: int

    def __init__(self):
        UnownedEntity.__init__(self)


class Grass(Terrain):
    _name = "Grass"
    _code_name = "grass"
    _defense = 1
    _initialized = False

    def __init__(self):
        Terrain.__init__(self)
