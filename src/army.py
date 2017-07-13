import entities


class Army(object):
    _name = NotImplemented
    _code_name = NotImplemented

    def __init__(self):
        pass

    def get_name(self):
        return self._name

    def get_code_name(self):
        return self._code_name


class IronLegion(Army):
    _name = "Iron Legion"
    _code_name = "iron_legion"

    def __init__(self):
        Army.__init__(self)


class HQ(entities.Building):
    _name = "HQ"
    _code_name = "HQ"

    def __init__(self, player, army):
        entities.Building.__init__(self, player, army)
