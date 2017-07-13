from army import Army
import entities

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