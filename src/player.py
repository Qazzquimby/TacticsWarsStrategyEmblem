import colors
from army import Army


class Player(object):
    def __init__(self, player_number: int, army: Army):
        self.player_number = player_number  # type: int
        self._color = self._init_color()  # type: colors.ArmyColor
        self._army = army  # type: Army

    def get_color(self) -> colors.ArmyColor:
        return self._color

    def get_color_name(self) -> str:
        return self._color.name

    def get_army(self) -> Army:
        return self._army

    def _init_color(self):
        if self.player_number == 0:
            return colors.Red
        elif self.player_number == 1:
            return colors.Blue
        else:
            raise ValueError
