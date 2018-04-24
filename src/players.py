# MIT License
# Copyright (c) 2018 Toren James Darby
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Classes related to players and player management."""

import colors


class Player(object):
    """A player's representation in the game.

    Attributes:
        self.player_number (int): A unique identifier for the player.
    """

    def __init__(self, player_number):
        self.player_number = player_number
        self._color = self._init_color()

    @property
    def color(self):
        """colors.ArmyColor: The player's color. The color was generated based on player_number"""
        return self._color

    @property
    def color_name(self) -> str:
        """str: The name of the player's color."""
        return self._color.name

    def _init_color(self):
        if self.player_number == 0:
            return colors.RED
        elif self.player_number == 1:
            return colors.BLUE
        else:
            raise ValueError("Not built to handle that player number yet")


class PlayerManager(object):
    """Generates a list of players."""

    def __init__(self, number_of_players):
        self.player_list = []
        self.current_player_index = 0
        for i in range(number_of_players):
            self.player_list.append(Player(i))

    @property
    def current_player(self):
        """Player: The currently active player."""
        return self.player_list[self.current_player_index]

    def advance_player(self):
        """Increments the current player index to the next active player."""
        self.current_player_index = (self.current_player_index + 1) % len(self.player_list)
