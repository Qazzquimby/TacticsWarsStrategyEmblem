import colors


class Player(object):
    def __init__(self, player_number: int):
        self.player_number = player_number  # type: int
        self._color = self._init_color()  # type: colors.ArmyColor

    @property
    def color(self) -> colors.ArmyColor:
        return self._color

    @property
    def color_name(self) -> str:
        return self._color.name

    def _init_color(self):
        if self.player_number == 0:
            return colors.RED
        elif self.player_number == 1:
            return colors.BLUE
        else:
            raise ValueError("Not built to handle that player number yet")


class PlayerManager(object):
    def __init__(self, number_of_players):
        self.player_list = []
        for i in range(number_of_players):
            self.player_list.append(Player(i))
