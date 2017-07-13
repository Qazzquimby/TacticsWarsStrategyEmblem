class Session(object):
    def __init__(self):
        """Holds widely used game variables"""

        self._game_running = True
        self._connection_mode = None

        class ConnectionModes(object):
            HOTSEAT = 1
            ONLINE = 2

        self.connection_modes = ConnectionModes()

    @property
    def game_running(self) -> bool:
        return self._game_running

    def quit_game(self):
        self._game_running = False
