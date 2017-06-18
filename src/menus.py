# import src.options_menu
import abc

import pygame_toolbox.graphics

import src.colors
import src.input
import src.session
import src.settings


class MenuState(abc.ABC):
    def __init__(self):
        pass


class GameScreen(abc.ABC):
    def __init__(self, display, settings, session):
        """Abstract class for displays in the game
        @type display: src.display.Display
        @param display:
            Display object for surface and update reference.

        @type settings: src.settings.Settings
        @param settings:
            src.settings.Settings. the instance of the settings object

        @type session: src.session.Session

        name:
            str.  the name of the screen
        menu:
            src.options_menu.cOptionsMenu that the screen uses. None if no menu
        __receive_input:
            Internal function that may be set for use with menus.
        """
        self.display = display  # type: src.display.Display
        self.settings = settings  # type: src.settings.Settings
        self.session = session  # type: src.session.Session
        self.name = None  # type: str
        self.menu = None
        self.__receive_input = None

    # def build_menu(self, option_names: [str], option_functions):
    #     """Constructs a menu
    #
    #     Each index in options becomes a row of the menu.
    #     Each row is given an index starting with 0 from the top.
    #     """
    #     menu_options = []
    #     for i in range(len(option_names)):
    #         menu_options.append((option_names[i], i, None))
    #
    #     menu = src.options_menu.cOptionsMenu(
    #         50,
    #         50,
    #         20,
    #         5,
    #         "vertical",
    #         100,
    #         self.display.surface,
    #         menu_options)
    #     menu.set_center(True, True)
    #     menu.set_alignment("center", "center")
    #     rect_list, state = menu.update()
    #     self.display.update_rect(rect_list)
    #
    #     def function_switch(curr_input: src.input.Input):
    #         """Runs the option function for the currently selected option"""
    #         for option in range(len(option_functions)):
    #             if menu.selection == option:
    #                 option_functions[option](curr_input)
    #                 break
    #
    #     self.__receive_input = function_switch
    #     self.menu = menu

    def receive_input(self, curr_input: src.input.Input):
        print("Sending {} to {}".format(curr_input.name, self.name))
        self.__receive_input(curr_input)


class ConnectionScreen(GameScreen):
    def __init__(self, display, settings, session):

        GameScreen.__init__(self, display, settings, session)
        self.name = "Connection Screen"

        def local_hotseat(curr_input):
            if isinstance(curr_input, src.input.Confirm):
                self.session.connection_mode = \
                    self.session.connection_modes.HOTSEAT
            elif isinstance(curr_input, src.input.Up):
                self.menu.select_up()
            elif isinstance(curr_input, src.input.Down):
                self.menu.select_down()

        def online_play(curr_input):
            if isinstance(curr_input, src.input.Confirm):
                self.session.connection_mode = \
                    self.session.connection_modes.ONLINE
            elif isinstance(curr_input, src.input.Up):
                self.menu.select_up()
            elif isinstance(curr_input, src.input.Down):
                self.menu.select_down()

        def quit_game(curr_input):
            if isinstance(curr_input, src.input.Confirm):
                self.session.game_over = True
            elif isinstance(curr_input, src.input.Up):
                self.menu.select_up()
            elif isinstance(curr_input, src.input.Down):
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

    def update(self, clock):
        self.menu.update(self.display.display, clock)
        # TODO in GameScreen define a type for Actions, so that they can be
        # remembered
        #  and undone
