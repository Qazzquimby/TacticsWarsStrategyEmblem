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

"""Manages the cursor and commands to control it."""
import abc

import commands
import directions
import points
import sprites
import user_input


class MoveCursor(commands.Command, abc.ABC):
    """A an abstract command for moving the cursor to arbitrary points. Children specify which
    direction to move."""
    direction = NotImplemented

    def __init__(self, target, content):
        commands.Command.__init__(self, target, content)

    def _move_to(self, point):
        """Moves the cursor to a given map point.

        Args:
            point (points.MapPoint): The point the cursor is moved to.
        """
        self.target.location = point
        self.content.map_drawing.scroll_to_cursor()

    def center(self):
        """Center the cursor on the map."""
        self._move_to(points.MapPoint(int(self.content.map.width / 2),
                                      int(self.content.map.height / 2)))

    def execute(self):
        """Moves the cursor in the given direction."""
        new_tile = self.target.location.directed_neighbour(self.direction)
        if self.content.map.has_point(new_tile):
            self._move_to(new_tile)


class MoveCursorRight(MoveCursor):
    """Moves the cursor one space to the right."""
    direction = directions.RIGHT

    def __init__(self, target, content):
        MoveCursor.__init__(self, target, content)


class MoveCursorLeft(MoveCursor):
    """Moves the cursor one space to the left."""
    direction = directions.LEFT

    def __init__(self, target, content):
        MoveCursor.__init__(self, target, content)


class MoveCursorUp(MoveCursor):
    """Moves the cursor one space up."""
    direction = directions.UP

    def __init__(self, target, content):
        MoveCursor.__init__(self, target, content)


class MoveCursorDown(MoveCursor):
    """Moves the cursor one space down."""
    direction = directions.DOWN

    def __init__(self, target, content):
        MoveCursor.__init__(self, target, content)


class Cursor(object):
    """The cursor the player controls to interact with the map.

    Attributes:
        self.map (world_screen.Map): The map containing the cursor.
        self.location (points.MapPoint): The cursor's location on the map.
        self.sprite (sprites.Sprite): The cursor's sprite.
    """

    def __init__(self, world_map):
        self.map = world_map
        self.location = points.MapPoint(0, 0)
        self.sprite = sprites.SpriteAnimation("", "assets/cursor").sprite

    @staticmethod
    def receive_input(curr_input):
        """Controls the cursor based on user input.

        Args:
            curr_input (user_input.Input): The user's input.
        Returns (MoveCursor): A command to execute.
        """
        if curr_input == user_input.RIGHT:
            return MoveCursorRight
        elif curr_input == user_input.LEFT:
            return MoveCursorLeft
        elif curr_input == user_input.UP:
            return MoveCursorUp
        elif curr_input == user_input.DOWN:
            return MoveCursorDown
        else:
            return None
