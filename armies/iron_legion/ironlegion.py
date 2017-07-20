import armymod
import entities


class IronLegion(armymod.Army, armymod.ArmyPlugin):
    _name = "Iron Legion"
    _code_name = "iron_legion"
    _buildings = []
    _units = []

    def __init__(self):
        armymod.Army.__init__(self)


class HQ(entities.Building):
    _name = "HQ"
    _code_name = "hq"
    _army = IronLegion

    def __init__(self, player):
        entities.Building.__init__(self, player)


HQ(None)
