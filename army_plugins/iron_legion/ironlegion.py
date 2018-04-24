import armies
import entities
from classproperty import classproperty

class IronLegion(armies.Army, armies.ArmyPlugin):
    def __init__(self):
        armies.Army.__init__(self)

    @property
    def name(self):
        """str: The army's outwards facing name."""
        return "Iron Legion"

    @property
    def code_name(self):
        """str: The army's internal name."""
        return "iron_legion"


class HQ(entities.Building):
    def __init__(self, player):
        entities.Building.__init__(self, player)

    @classproperty
    def name(self):
        return "HQ"

    @classproperty
    def code_name(self):
        return "hq"

    @classproperty
    def army(self):
        return IronLegion

HQ(None)


class Marine(entities.Unit):
    animation_speed = 5

    def __init__(self, player):
        entities.Unit.__init__(self, player)

    @classproperty
    def name(self):
        return "Marine"

    @classproperty
    def code_name(self):
        return "marine"

    @classproperty
    def army(self):
        return IronLegion


Marine(None)
