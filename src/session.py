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

"""Global settings and constants hidden from the user."""

import enum


class Session(object):
    """Global settings and constants hidden from the user."""

    def __init__(self):
        """Holds widely used game variables"""

        self._game_running = True
        self._connection_mode = None

        class ConnectionModes(enum.Enum):
            """Methods through which players can connect to each other."""
            hot_seat = enum.auto()
            online = enum.auto()

        self.connection_modes = ConnectionModes

    @property
    def game_running(self):
        """bool: If the game is still running. Checked each frame."""
        return self._game_running

    def quit_game(self):
        """Set the game to stop running."""
        self._game_running = False
