import typing

import pygame

import armymod
import graphics
import importer
import screens
import sessionmod
import user_input
import world_screen


class Button(object):
    def __init__(self, menu, text, confirm_function):
        if text is not None:
            self.text = text
        if confirm_function is not None:
            self.confirm = confirm_function

        self.menu = menu
        self.rect = NotImplemented
        self.offset = NotImplemented

        self.is_image = False

    def receive_input(self, curr_input: user_input.Input):
        if isinstance(curr_input, user_input.Confirm):
            self.confirm()

        elif isinstance(curr_input, user_input.Up):
            self.menu.select_up()

        elif isinstance(curr_input, user_input.Down):
            self.menu.select_down()

    def confirm(self):
        pass  # May be overwritten in init


class SelectionButton(Button):
    def __init__(self, menu, button_list: typing.List[Button]):
        if len(button_list) == 0:
            raise ValueError("Button list empty")
        Button.__init__(self, menu, None, None)
        self.button_list = button_list
        self.selection = 0

    @property
    def selected_button(self):
        return self.button_list[self.selection]

    @property
    def text(self):
        try:
            return self.selected_button.text
        except AttributeError:
            raise AttributeError("One of the selection button's buttons was given None as its "
                                 "text.")

    @property
    def confirm(self):
        return self.selected_button.confirm

    def receive_input(self, curr_input: user_input.Input):
        if curr_input == user_input.Confirm:
            self.confirm()

        elif curr_input == user_input.Up:
            self.menu.select_up()

        elif curr_input == user_input.Down:
            self.menu.select_down()

        elif curr_input == user_input.Left:
            self.left_choose_option()

        elif curr_input == user_input.Right:
            self.right_choose_option()

    def left_choose_option(self):
        self.selection = (self.selection - 1) % len(self.button_list)
        self.menu.rewrite_buttons()

    def right_choose_option(self):
        self.selection = (self.selection + 1) % len(self.button_list)
        self.menu.rewrite_buttons()


class Menu(object):
    def __init__(self, background: pygame.Surface, button_list: typing.List[Button]):

        self.draw_surface = background  # Surface to draw to
        self.background = background.copy()  # The unedited background image

        self.menu_items = []  # List of content items

        self.font = pygame.font.Font(None, 32)  # Font to use
        self._unselected_color = graphics.WHITE  # Color for unselected text
        self._selected_color = graphics.RED  # Color for selected text
        self.image_highlight_color = graphics.RED  # Color for the image highlights
        self.image_highlight_offset = 2  # Addition padding around image

        self.update_buttons = True  # True if the positions of the buttons need to be updated
        self.refresh_whole_surface_on_load = False  # When the content is first displayed

        self.selection = 0  # The currently selected button
        self.selection_prev = 0
        self.add_buttons(button_list)
        self.update(self.selection)

    @property
    def current_text(self):
        return self.menu_items[self.selection]['text']

    @property
    def current_image(self):
        return self.menu_items[self.selection]['b_image']

    @property
    def unselected_color(self):
        return self._unselected_color

    @unselected_color.setter
    def unselected_color(self, new_color):
        self._unselected_color = new_color
        self.update_buttons = True

    @property
    def selected_color(self):
        return self._selected_color

    @selected_color.setter
    def selected_color(self, new_color):
        self._selected_color = new_color
        self.update_buttons = True

    @property
    def selected_button(self):
        return self.menu_items[self.selection]

    def add_buttons(self, button_list):
        for button in button_list:
            self.menu_items.append(self.create_button(button))
        self.update_buttons = True
        self.update_button_locations()
        self.set_button_images()

    def remove_buttons(self, index_list):
        for index in index_list:
            if len(self.menu_items) > 0:
                self.menu_items.pop(index)
        self.update_buttons = True

    def update_button_locations(self):
        if len(self.menu_items) > 0:
            self.position_buttons()
        self.set_button_images()
        self.update_buttons = False

    def create_button(self, button):
        width, height = self.font.size(button.text)
        button.rect = pygame.Rect((0, 0), (width, height))
        return button

    def set_button_images(self):
        for button in self.menu_items:
            self.set_button_image(button)

    def set_button_image(self, button):
        # If this button is not an image, create the selected and unselected
        # images based on the text
        if not button.is_image:
            font_render = self.font.render
            width = button.rect[2]
            height = button.rect[3]
            rect = pygame.Rect(button.offset, (width, height))

            selected_image = pygame.Surface((width, height), -1).convert()
            selected_image.blit(self.background, (0, 0), rect)
            text_image = font_render(button.text, True, self._selected_color)
            selected_image.blit(text_image, (0, 0))

            unselected_image = pygame.Surface((width, height), -1).convert()
            unselected_image.blit(self.background, (0, 0), rect)
            text_image = font_render(button.text, True, self._unselected_color)
            unselected_image.blit(text_image, (0, 0))

        # Else this button is a graphic button, so create the selected and
        # unselected images based on the image provided
        else:
            orig_width, orig_height = button['b_image'].get_size()
            new_width = button.rect[2]
            new_height = button.rect[3]
            offset = (
                self.image_highlight_offset, self.image_highlight_offset)

            selected_image = pygame.Surface((new_width, new_height), -1).convert()
            selected_image.fill(self.image_highlight_color)
            rect = pygame.Rect((button['offset'][0] + offset[0],
                                button['offset'][1] + offset[1]),
                               (orig_width, orig_height))
            selected_image.blit(self.background, offset, rect)
            selected_image.blit(button['b_image'], offset)

            unselected_image = pygame.Surface((new_width, new_height), -1).convert()
            rect = pygame.Rect(button['offset'], (new_width, new_height))
            unselected_image.blit(self.background, (0, 0), rect)
            unselected_image.blit(button['b_image'], offset)

        button.s_image = selected_image
        button.u_image = unselected_image

    def position_buttons(self):
        max_width = 0
        max_height = 0
        counter = 0
        y_loc = 0

        # Get the maximum width and height of the surfaces
        for button in self.menu_items:
            width = button.rect[2]
            height = button.rect[3]
            max_width = max(width, max_width)
            max_height = max(height, max_height)

        # Position the button in relation to each other
        for button in self.menu_items:
            offset_height = (max_height - button.rect[3]) / 2
            offset_width = (max_width - button.rect[2]) / 2

            # Assign the location of the button
            button.offset = (offset_width, y_loc + offset_height)
            y_loc += max_height
            counter += 1

        # Move the buttons to make them centered
        for button in self.menu_items:
            shift_x = 0 - (self.draw_surface.get_rect()[2] - button.rect[2]) / 2
            shift_y = 0 - (self.draw_surface.get_rect()[3] - button.rect[3]) / 2

            button.offset = (-shift_x, button.offset[1] - shift_y)

    def update(self, c_state=-1):
        self.selection_prev = self.selection
        self.selection = c_state

        # Should be the first transition when the content is made, and sets up the content
        if c_state == -1:
            c_state = 0  # default button (starts at topmost button)
            self.selection = 0
            if self.refresh_whole_surface_on_load:
                pygame.Rect((0, 0), self.draw_surface.get_size())
            return c_state

        self.draw_buttons()
        return c_state

    def rewrite_buttons(self):
        for button in self.menu_items:
            width, height = self.font.size(button.text)
            button.rect = pygame.Rect((0, 0), (width, height))
            self.update_button_locations()
            self.set_button_images()

    def draw_buttons(self):
        # Cycle through the buttons, only draw the ones that need to be redrawn
        self.draw_surface.blit(self.background, (0, 0))
        for button in self.menu_items:
            if self.selected_button == button:
                image = button.s_image
            else:
                image = button.u_image

            self.draw_surface.blit(image, button.offset, button.rect)

    def receive_input(self, curr_input: user_input.Input):
        self.selected_button.receive_input(curr_input)

    def select_up(self):
        """Moves to the selection one higher, or loops to the bottom"""
        self.update((self.selection - 1) % len(self.menu_items))

    def select_down(self):
        """Moves to the selection one lower, or loops to the top"""
        self.update((self.selection + 1) % len(self.menu_items))

    def destroy_everything(self):
        while len(self.menu_items) > 0:
            self.remove_buttons([len(self.menu_items) - 1])
        self.draw_buttons()


class ArmySelectMenu(Menu):
    def __init__(self, display, session):
        self.display = display
        self.session = session

        self.army_importer = armymod.ArmyImporter()
        self.armies = self.army_importer.plugins

        army_buttons = [Button(self, army.name, self.army_confirm_factory(army)) for army in
                        self.armies]

        button_list = [SelectionButton(self, army_buttons),
                       Button(self, "Quit", self.quit_game)]

        background = display.surface
        Menu.__init__(self, 5, background, button_list)

    def army_confirm_factory(self, army):
        def army_confirm_function():
            print(army.name)

        return army_confirm_function

    def quit_game(self):
        self.session.game_over = True


class MapSelectMenu(Menu):
    def __init__(self, screen_engine: screens.ScreenEngine):
        self.screen_engine = screen_engine  # type: screens.ScreenEngine
        self.display = screen_engine.display  # type: graphics.Display
        self.session = screen_engine.session  # type: sessionmod.Session

        self.map_importer = importer.MapImporter(["../maps"])
        self.world_setups = self.map_importer.plugins

        map_buttons = [
            Button(self, world_setup.map_setup.name, self.world_setup_confirm_factory(world_setup))
            for world_setup in self.world_setups]

        button_list = [SelectionButton(self, map_buttons),
                       Button(self, "Quit", self.quit_game)]

        background = self.display.surface
        Menu.__init__(self, background, button_list)

    def world_setup_confirm_factory(self, world_setup):
        def world_setup_confirm_function():
            main_screen = world_screen.MainGameScreen(self.screen_engine, world_setup)
            self.screen_engine.push_screen(main_screen)

        return world_setup_confirm_function

    def quit_game(self):
        self.session.quit_game()


class MenuScreen(screens.GameScreen):
    def __init__(self, screen_engine: screens.ScreenEngine):
        screens.GameScreen.__init__(self, screen_engine)

    def execute_tick(self):
        self.content.draw_buttons()

    def _receive_input(self, curr_input: user_input.Input):
        self.content.receive_input(curr_input)

    def exit(self):
        self.content.destroy_everything()


class MapSelectScreen(MenuScreen):
    def __init__(self, screen_engine: screens.ScreenEngine):
        screens.GameScreen.__init__(self, screen_engine)
        self.content = MapSelectMenu(screen_engine)
        self.name = "Map Selection Screen"
