# import src.options_menu
import abc

import pygame_toolbox.graphics

import src.colors
import src.user_input
import src.session
import src.screen


class MenuState(abc.ABC):
    def __init__(self):
        pass


class ConnectionScreen(src.screen.GameScreen):
    def __init__(self, display, session):

        src.screen.GameScreen.__init__(self, display, session)
        self.name = "Connection Screen"

        def local_hotseat(curr_input):
            if isinstance(curr_input, src.user_input.Confirm):
                self.session.connection_mode = self.session.connection_modes.HOTSEAT
            elif isinstance(curr_input, src.user_input.Up):
                self.menu.select_up()
            elif isinstance(curr_input, src.user_input.Down):
                self.menu.select_down()

        def online_play(curr_input):
            if isinstance(curr_input, src.user_input.Confirm):
                self.session.connection_mode = \
                    self.session.connection_modes.ONLINE
            elif isinstance(curr_input, src.user_input.Up):
                self.menu.select_up()
            elif isinstance(curr_input, src.user_input.Down):
                self.menu.select_down()

        def quit_game(curr_input):
            if isinstance(curr_input, src.user_input.Confirm):
                self.session.game_over = True
            elif isinstance(curr_input, src.user_input.Up):
                self.menu.select_up()
            elif isinstance(curr_input, src.user_input.Down):
                self.menu.select_down()

        class ConnectionMenu(pygame_toolbox.graphics.Menu):
            def __init__(self):
                size = (display.display_width, display.display_width)
                header = "Header"
                buttons = [["Local Hotseat", local_hotseat],
                           ["Online Play", online_play],
                           ["Quit", quit_game]]
                pygame_toolbox.graphics.Menu.__init__(
                    self,
                    size,
                    src.colors.BLACK,
                    header,
                    buttons)

        self.menu = ConnectionMenu()

    def execute_tick(self):
        raise NotImplementedError

    def update(self, clock):
        self.menu.update(self.display.display, clock)
        # TODO in GameScreen define a type for Actions, so that they can be
        # remembered
        #  and undone
