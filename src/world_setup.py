import player
from army import Army


class WorldSetup(object):
    def __init__(self):
        self._players = []
        self._map_path = "../maps/map_filename.xml"

    @property
    def map_path(self):
        return self._map_path

    def add_player(self, army: Army):
        new_player_number = len(self._players)
        new_player = player.Player(new_player_number, army)
        self._players.append(new_player)

        # todo current player
        # todo next player
