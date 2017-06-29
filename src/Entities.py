
class Entity(object):
    def __init__(self):
        pass


class Grass(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.name = "Grass"
        self.defense = 1
        self.sprite = None

class NullEntity(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.name = "NULL ENTITY"