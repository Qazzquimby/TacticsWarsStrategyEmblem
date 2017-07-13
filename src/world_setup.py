import player
import army


class WorldSetup(object):
    def __init__(self):
        self._players = []
        self._map_path = "../maps/map_filename.xml"

    def get_map_path(self):
        return self._map_path

    def add_player(self, army: army.Army()):
        new_player_number = len(self._players)
        new_player = player.Player(new_player_number, army)
        self._players.append(new_player)

        # todo current player
        # todo next player