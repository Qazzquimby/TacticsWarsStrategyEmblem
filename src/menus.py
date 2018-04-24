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

"""Classes related to menus outside of the main game screen."""
import abc
import typing

import pygame

import armies
import graphics
import importer
import screens
import user_input
import world_screen


class Button(object):
    """A button in a menu

    Attributes:
        self.text (str): The text displayed in the button.
        self.confirm (function): The function ran when the button is used.
        self.menu (Menu): The menu the button belongs to.
    """

    def __init__(self, menu, text, confirm_function):
        if text is not None:
            self.text = text
        if confirm_function is not None:
            self.confirm = confirm_function

        self.menu = menu

    def receive_input(self, curr_input):
        """Calls function mapped to the given input.

        Args:
            curr_input (user_input.Input): The routed input.
        """
        if curr_input == user_input.CONFIRM:
            self.confirm()

        elif curr_input == user_input.UP:
            self.up()

        elif curr_input == user_input.DOWN:
            self.down()

        elif curr_input == user_input.LEFT:
            self.left()

        elif curr_input == user_input.RIGHT:
            self.right()

    def confirm(self):  # pylint: disable=method-hidden
        """Called when confirm input is sent to button."""
        pass  # May be overwritten in init

    def up(self):
        """Called when up input is sent to button."""
        self.menu.select_up()

    def down(self):
        """Called when down input is sent to button."""
        self.menu.select_down()

    def right(self):
        """Called when right input is sent to button."""
        pass

    def left(self):
        """Called when left input is sent to button."""
        pass


class SelectionButton(Button):
    """A button which holds other buttons, and can scroll between them using left and right.

    Attributes:
        self.button_list (List[Button]): The buttons this displays.
        self._selection (int): The index of the currently selected button.
    """

    def __init__(self, menu, button_list: typing.List[Button]):
        if not button_list:
            raise ValueError("Button list empty")
        Button.__init__(self, menu, None, None)
        self.button_list = button_list
        self.selection = 0

    @property
    def selected_button(self):
        """Button: The currently selected button."""
        return self.button_list[self.selection]

    @property
    def text(self):
        """str: The text of the currently selected button."""
        try:
            return self.selected_button.text
        except AttributeError:
            raise AttributeError("One of the _selection button's buttons was given None as its "
                                 "text.")

    def confirm(self):  # pylint: disable=method-hidden
        """Send confirm the selected button."""
        self.selected_button.confirm()

    def left(self):
        """Select the previous button."""
        self.selection = (self.selection - 1) % len(self.button_list)
        self.menu.rewrite_buttons()

    def right(self):
        """Select the next button."""
        self.selection = (self.selection + 1) % len(self.button_list)
        self.menu.rewrite_buttons()


# noinspection PyArgumentList
class Menu(object):  # pylint: disable=too-many-instance-attributes
    """A collection of buttons with functionality to display them.

    Attributes:
        self.draw_surface (pygame.Surface): The surface to draw the menu to.
        self.background (pygame.Surface): A backup copy of the draw_surface.
        self._buttons (list(Button)): The buttons in the menu, in order of their positions.
        self.font (pygame.font.Font): The font to display the text of the buttons.
        self.image_highlight_color (graphics.Color): The color to highlight selected image
        buttons in.
        self.image_highlight_offset (int): Amount of additional padding to put around selected
        image buttons.
        self._selection (int): The currently selected button index.
        self._selection_prev (int): The previously selected button index.

    """

    def __init__(self, background, button_list):
        self.draw_surface = background
        self.background = background.copy()

        self.font = pygame.font.Font(None, 32)
        self.unselected_color = graphics.WHITE
        self.selected_color = graphics.RED

        self._buttons = []
        self._button_rects = {}
        self._button_offsets = {}
        self._s_images = {}
        self._u_images = {}

        self._selection = 0
        self._selection_prev = 0

        self.add_buttons(button_list)
        self.update(self._selection)

    @property
    def selected_button(self):
        """Button: The currently selected button."""
        return self._buttons[self._selection]

    @property
    def current_text(self):
        """str: The text of the currently selected button."""
        return self.selected_button['text']

    @property
    def current_image(self):
        """pygame.Surface: The image of the currently selected button."""
        return self.selected_button['b_image']

    def add_buttons(self, button_list):
        """Adds the buttons in the button_list to the menu.

        Args:
            button_list (List[Button]): List of buttons to add.
        """
        for button in button_list:
            self._buttons.append(self.set_button_rect(button))
        self.update_button_locations()
        self.set_button_images()

    def remove_buttons(self, index_list):
        """Remove buttons from the given indices.

        Args:
            index_list (list[int]): The indices of the buttons to remove.
        """

        self._buttons = [menu_item for i, menu_item in enumerate(self._buttons)
                         if i not in index_list]

    def update_button_locations(self):
        """Reposition all buttons."""
        if self._buttons:
            self.position_buttons()
        self.set_button_images()

    def set_button_rect(self, button):
        """Sets the rect attribute of the given button.

        Args:
            button (Button): The button to set up.

        Returns:
            Button: The passed button.
        """
        width, height = self.font.size(button.text)
        self._button_rects[button] = pygame.Rect((0, 0), (width, height))
        return button

    def set_button_images(self):
        """Generates the image for each button."""
        for button in self._buttons:
            self.set_button_image(button)

    def set_button_image(self, button):
        """Generates an image of the button contents, positioned on screen.

        Args:
            button (Button): The button to generate.
        """
        font_render = self.font.render

        width = self.button_width(button)
        height = self.button_height(button)
        rect = pygame.Rect(self._button_offsets[button], (width, height))

        # pylint: disable=too-many-function-args
        selected_image = pygame.Surface((width, height), -1).convert()
        selected_image.blit(self.background, (0, 0), rect)
        text_image = font_render(button.text, True, self.selected_color)
        selected_image.blit(text_image, (0, 0))
        unselected_image = pygame.Surface((width, height), -1).convert()

        unselected_image.blit(self.background, (0, 0), rect)
        text_image = font_render(button.text, True, self.unselected_color)
        unselected_image.blit(text_image, (0, 0))

        self._s_images[button] = selected_image
        self._u_images[button] = unselected_image

    def position_buttons(self):
        """Gets the screen positions to draw the buttons to, based on their order and size."""
        max_width = 0
        max_height = 0
        counter = 0
        y_loc = 0

        # Get the maximum width and height of the surfaces
        for button in self._buttons:
            width = self.button_width(button)
            height = self.button_height(button)
            max_width = max(width, max_width)
            max_height = max(height, max_height)

        # Position the button in relation to each other
        for button in self._buttons:
            offset_height = (max_height - self.button_height(button)) / 2
            offset_width = (max_width - self.button_width(button)) / 2

            # Assign the location of the button
            self._button_offsets[button] = (offset_width, y_loc + offset_height)
            y_loc += max_height
            counter += 1

        # Move the buttons to make them centered
        for button in self._buttons:
            shift_x = 0 - (self.draw_surface.get_rect()[2] - self.button_width(button)) / 2
            shift_y = 0 - (self.draw_surface.get_rect()[3] - self.button_height(button)) / 2

            self._button_offsets[button] = (-shift_x, self._button_offsets[button][1] - shift_y)

    def update(self, new_selected_button):
        """Redraws the menu based on its current state. Called whenever the menu changes appearance.
        Args:
            new_selected_button (int): The currently selected menu item.

        Returns:

        """
        self._selection_prev = self._selection
        self._selection = new_selected_button

        self.draw_buttons()
        return new_selected_button

    def rewrite_buttons(self):
        """Regenerates button's images based on their current states."""
        for button in self._buttons:
            width, height = self.font.size(button.text)
            self._button_rects[button] = pygame.Rect((0, 0), (width, height))
            self.update_button_locations()
            self.set_button_images()

    def draw_buttons(self):
        """Draws all buttons to the screen."""
        self.draw_surface.blit(self.background, (0, 0))
        for button in self._buttons:
            if self.selected_button == button:
                image = self._s_images[button]
            else:
                image = self._u_images[button]

            self.draw_surface.blit(image, self._button_offsets[button], self._button_rects[button])

    def receive_input(self, curr_input):
        """Route input to the currently selected button.

        Args:
            curr_input (user_input.Input): The input to route.
        """
        self.selected_button.receive_input(curr_input)

    def select_up(self):
        """Moves to the _selection one higher, or loops to the bottom"""
        self.update((self._selection - 1) % len(self._buttons))

    def select_down(self):
        """Moves to the _selection one lower, or loops to the top"""
        self.update((self._selection + 1) % len(self._buttons))

    def clear(self):
        """Remove all buttons from the menu."""
        while self._buttons:
            self.remove_buttons([len(self._buttons) - 1])
        self.draw_buttons()

    def button_width(self, button):
        """Returns the width of the button's rect.

        Args:
            button (Button)
        Returns:
            int: The width.
        """
        return self._button_rects[button][2]

    def button_height(self, button):
        """Returns the height of the button's rect.

        Args:
            button (Button)
        Returns:
            int: The height.
        """
        return self._button_rects[button][3]


class ArmySelectMenu(Menu):
    """A menu for players to select their army.

    Attributes:
        self.display (graphics.Display): Handles drawing to the screen.
        self.session (Session): Holds commonly used global variables.
        self.armies (List[armies.Army]): List of all imported armies.
    """

    def __init__(self, display, session):
        self.display = display
        self.session = session

        self.armies = armies.ArmyImporter().plugins

        army_buttons = [Button(self, army.name, self.army_confirm_factory(army)) for army in
                        self.armies]

        button_list = [SelectionButton(self, army_buttons),
                       Button(self, "Quit", self.quit_game)]

        background = display.surface
        Menu.__init__(self, background, button_list)

    @staticmethod
    def army_confirm_factory(army):
        """Generates a confirm function for an army's button. Confirming will select the army for
        the player.

        Args:
            army (armies.Army): The army to generate a confirm function for.

        Returns:
            function: The confirm function.
        """

        def army_confirm_function():
            """Selects the army for the current player."""
            print(army.name)  # todo implement actual function.

        return army_confirm_function

    def quit_game(self):
        """Ends the game."""
        self.session.game_over = True


class MapSelectMenu(Menu):
    """A menu for selecting the map the game will take place on.

    Attributes:
        self.screen_engine(screens.ScreenEngine): Handles transitions between screens.
        self.display (graphics.Display): Handles drawing to the screen.
        self.session (Session): Holds commonly used global variables.

        self.world_setups(WorldSetup): All imported maps.
    """

    def __init__(self, screen_engine: screens.ScreenEngine):
        self.screen_engine = screen_engine
        self.display = screen_engine.display
        self.session = screen_engine.session

        self.world_setups = importer.MapImporter(["../maps"]).plugins  # pylint: disable=no-member

        map_buttons = [
            Button(self, world_setup.map_setup.name, self.world_setup_confirm_factory(world_setup))
            for world_setup in self.world_setups]

        button_list = [SelectionButton(self, map_buttons),
                       Button(self, "Quit", self.quit_game)]

        background = self.display.surface
        Menu.__init__(self, background, button_list)

    def world_setup_confirm_factory(self, world_setup):
        """Generates a confirm function for a map's button. Confirming will select the map to be
        played on.

                Args:
                    world_setup (WorldSetup): The map to choose.

                Returns:
                    function: The confirm function.
                """

        def world_setup_confirm_function():
            """Loads the selected map."""
            main_screen = world_screen.MainGameScreen(self.screen_engine, world_setup)
            self.screen_engine.push_screen(main_screen)

        return world_setup_confirm_function

    def quit_game(self):
        """Exits the game."""
        self.session.quit_game()


class MenuScreen(screens.GameScreen, abc.ABC):
    """A game screen consisting of menu.
    Attributes:
        self.content (Menu): The menu displayed in the screen.
    """

    def __init__(self, screen_engine: screens.ScreenEngine, content):
        super().__init__(screen_engine)
        self.content = content

    def execute_tick(self):
        """Draws the button each tick."""
        self.content.draw_buttons()

    def _receive_input(self, curr_input: user_input.Input):
        self.content.receive_input(curr_input)

    def exit(self):
        """Deletes all buttons from the menu upon exiting the screen."""
        self.content.clear()


class MapSelectScreen(MenuScreen):
    """A menu screen consisting of a map selection menu."""

    def __init__(self, screen_engine: screens.ScreenEngine):
        content = MapSelectMenu(screen_engine)
        MenuScreen.__init__(self, screen_engine, content)

        self.name = "Map Selection Screen"
