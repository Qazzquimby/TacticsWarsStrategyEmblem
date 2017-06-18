

class Session(object):
    def __init__(self):
        """Holds widely used game variables"""

        self.game_over = False
        self.connection_mode = None

        class ConnectionModes(object):
            HOTSEAT = 1
            ONLINE = 2

        self.connection_modes = ConnectionModes()