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

"""Holds screens and screen management."""

import abc

import user_input


class ScreenEngine(object):
    """Manages the current state and backing into previous states.

    Attributes:
        self.display (graphics.Display): The display the screen should draw to.
        self.session (session.Session): Holds commonly used global variables.
    """

    def __init__(self, display, session):
        self._screen_stack = []
        self.display = display
        self.session = session

    @property
    def screen(self):
        """GameScreen:Gets the current screen. Exits the game if there is no screen."""
        if not self._screen_stack:
            self.quit_game()
            return EmptyScreen()
        return self._screen_stack[len(self._screen_stack) - 1]

    def push_screen(self, screen):
        """Transitions to a new screen, such that the previous screen can be backed into.

        Args:
            screen (GameScreen): The screen to transition to.
        """
        if self._screen_stack:
            self.screen.exit()
        self._screen_stack.append(screen)
        self.screen.enter()

    def pop_screen(self):
        """Backs out to the previous screen."""
        self.screen.exit()
        try:
            self._screen_stack.pop(len(self._screen_stack) - 1)
        except IndexError:
            pass
        self.screen.enter()

    def switch_screen(self, screen):
        """Backs out to the previous screen, then enter a new screen.

        Args:
            screen (GameScreen): The screen to transition to.
        """
        self.pop_screen()
        self.push_screen(screen)

    def execute_tick(self, current_input: user_input.Input):
        """Ran every tick. Routes input and executes the current screen's per tick function.

        Args:
            current_input (user_input.Input): The input to route.
        """
        self.receive_input(current_input)
        self.screen.execute_tick()

    def receive_input(self, current_input):
        """Routes input to the current screen.

        Args:
            current_input (user_input.Input): The input to route.
        """
        if current_input:
            self.screen.receive_input(current_input)

    def quit_game(self):
        """Set the game to end."""
        self.session.quit_game()


class GameScreen(abc.ABC):
    """An ABC for screens.

    Attributes:
        self.screen_engine(ScreenEngine): The screen engine the screen belongs to.
        self.display (graphics.Display): The display to draw to.
        self.session (session.Session): Commonly used global variables.
        self.name (str): An identifying name for the screen.
        self.content (any): The contents of the screen, to be interacted with in execute_tick and
            self._receive_input()
    """

    def __init__(self, screen_engine):
        self.screen_engine = screen_engine
        self.display = screen_engine.display
        self.session = screen_engine.session
        self.name = NotImplemented
        self.content = NotImplemented

    def receive_input(self, curr_input):
        """Logs input, then routes it to the overwritten _receive_input function.

        Args:
            curr_input (user_input.Input): The input to be routed.
        """
        print("Sending {} to {}".format(curr_input.name, self.name))
        self._receive_input(curr_input)

    def execute_tick(self):
        """Overwritten function called every tick to update the screen."""
        raise NotImplementedError

    def _receive_input(self, curr_input):
        raise NotImplementedError

    def enter(self):
        """Performed when entering the screen."""
        pass

    def exit(self):
        """Performed when exiting the screen."""
        pass


class EmptyScreen(GameScreen):
    """A screen without content for edge cases, such as when the game is exiting."""

    # noinspection PyMissingConstructor
    def __init__(self):  # pylint: disable=super-init-not-called
        # Initialized before screen_engine, so does not run GameScreen.__init__ which requires it.
        pass

    def execute_tick(self):
        """Does not update."""
        pass

    def _receive_input(self, curr_input: user_input.Input):
        pass
