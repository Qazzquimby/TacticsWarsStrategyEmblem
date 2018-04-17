import armies
import entities


class IronLegion(armies.Army, armies.ArmyPlugin):
    _name = "Iron Legion"
    _code_name = "iron_legion"
    _buildings = []
    _units = []

    def __init__(self):
        armies.Army.__init__(self)


class HQ(entities.Building):
    _name = "HQ"
    _code_name = "hq"
    _army = IronLegion

    def __init__(self, player):
        entities.Building.__init__(self, player)


HQ(None)


class Marine(entities.Unit):
    _name = "Marine"
    _code_name = "marine"
    _army = IronLegion
    animation_speed = 5

    def __init__(self, player):
        entities.Unit.__init__(self, player)


Marine(None)
