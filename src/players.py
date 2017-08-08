import armymod
import colors


class Player(object):
    def __init__(self, player_number: int, army: "armymod.Army"):
        self.player_number = player_number  # type: int
        self._color = self._init_color()  # type: colors.ArmyColor
        self._army = army  # type: armymod.Army

    @property
    def color(self) -> colors.ArmyColor:
        return self._color

    @property
    def color_name(self) -> str:
        return self._color.name

    @property
    def army(self) -> "armymod.Army":
        return self._army

    def _init_color(self):
        if self.player_number == 0:
            return colors.Red
        elif self.player_number == 1:
            return colors.Blue
        else:
            raise ValueError
