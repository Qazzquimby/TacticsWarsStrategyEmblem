# !/usr/bin/env python3

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

"""Main game loop.

This module initializes core aspects of the game engine, and updates the game
in a loop based on the frame rate.

Attributes:
    PROFILE (boolean): If the game loop should log profiling information.
"""

import cProfile

import pygame

import graphics
import menus
import screens
import user_input
from session import Session
from settings import Settings  # pylint: disable=no-name-in-module

SETTINGS = Settings()

PROFILE = False  # Keep profiler metrics each frame


class Clock(object):
    """Simple clock for the game loop."""

    def __init__(self):
        self._pygame_clock = pygame.time.Clock()

    @property
    def ms_per_frame(self):
        """int: Returns the number of milliseconds in a frame."""
        return int(1000 / SETTINGS.fps)

    def wait_for_next_tick(self):
        """Waits until there have been ms_per_frame milliseconds since the last tick.
        Wait until the correct time. Does not apply a flat wait time."""
        self._pygame_clock.tick(SETTINGS.fps)


class Main(object):
    """Top level of game engine.

    Holds and initializes main systems, and runs the main game loop.

    Attributes:
        self.session (Session): Session wide variables.
        self.display (graphics.Display): Core graphics functionality.
        self.screen_engine (screens.ScreenEngine): Manages state among screens and menus.
        self.clock (Clock): Simple clock for the game loop.
        self.input_interpreter (user_input.InputInterpreter): Reads and acts on user input.
    """

    def __init__(self):
        pygame.init()  # pylint: disable=no-member
        pygame.display.set_caption("Tactics Wars Strategy Emblem")

        self.session = Session()
        self.display = graphics.Display()
        self.screen_engine = self.init_screen_engine()
        self.clock = Clock()
        self.input_interpreter = user_input.InputInterpreter()

        self.run_game()

    def init_screen_engine(self):
        """Initializes a screens.ScreenEngine for the session to the starting screen.

        Returns:
            screens.ScreenEngine: The initialized screen engine.
        """
        screen_engine = screens.ScreenEngine(self.display, self.session)
        initial_screen = menus.MapSelectScreen(screen_engine)
        screen_engine.push_screen(initial_screen)
        return screen_engine

    def run_game(self):
        """Runs the game loop until terminated, then uninitializes."""
        self.game_loop()
        self.uninit()

    def game_loop(self):
        """Runs the game loop until the game is ended."""
        if PROFILE:
            execute_func = self.execute_and_profile_tick
        else:
            execute_func = self.execute_tick

        while self.session.game_running:
            execute_func()

    def execute_and_profile_tick(self):
        """Wraps profiling code around execute_tick.
        Stats dumped to the file 'profile_output'."""
        profiler = cProfile.Profile(builtins=False)
        profiler.enable()

        self.execute_tick()

        profiler.disable()
        profiler.create_stats()
        profiler.print_stats()
        profiler.dump_stats("profile_output")

    def execute_tick(self):
        """Reads input, then updates the screen engine, display, and waits for the next tick."""
        current_input = self.input_interpreter.interpret_input()
        if current_input == user_input.QUIT:
            self.session.quit_game()
        self.screen_engine.execute_tick(current_input)
        self.display.execute_tick()
        self.clock.wait_for_next_tick()

    @staticmethod
    def uninit():
        """Prepares program to close and closes."""
        pygame.quit()  # pylint: disable=no-member


if __name__ == "__main__":
    MAIN = Main()
