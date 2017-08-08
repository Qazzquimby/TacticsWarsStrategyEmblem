import abc
import typing

import pygame

import armymod
import graphics
import screens
import user_input


class MenuState(abc.ABC):
    def __init__(self):
        pass


class MapScreen(screens.GameScreen):
    def _receive_input(self, curr_input: user_input.Input):
        pass

    def execute_tick(self):
        pass


class Menu(object):
    def __init__(self,
                 wrap_length: int,
                 background: pygame.Surface,
                 button_list: typing.List["Button"]):

        self.wrap_length = wrap_length  # number of items before wrapping
        self.background = background.copy()  # The unedited background image

        self.menu_items = []  # List of content items
        self.font = pygame.font.Font(None, 32)  # Font to use

        self._unselected_color = graphics.WHITE  # Color for unselected text
        self._selected_color = graphics.RED  # Color for selected text
        self.image_highlight_color = graphics.RED  # Color for the image highlights
        self.image_highlight_offset = 2  # Addition padding around image

        self.draw_surface = background  # Surface to draw to
        self.centered = True
        self.centeredOnScreen = True  # True if the content is centered
        self.update_buttons = True  # True if the positions of the buttons need to be updated
        self.refresh_whole_surface_on_load = False  # When the content is first displayed

        self.alignment = {'vertical': 'top',
                          'horizontal': 'center'}

        self.selection = 0  # The currently selected button
        self.selection_prev = 0
        self.add_buttons(button_list)
        self.update(self.selection)

    def get_current_text(self):
        return self.menu_items[self.selection]['text']

    def get_current_image(self):
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

    def add_buttons(self, button_list):
        for button in button_list:
            self.menu_items.append(self.create_button(button))
        self.update_buttons = True
        self.update_button_locations()
        self.set_button_images()

    @property
    def selected_button(self):
        return self.menu_items[self.selection]

    def remove_buttons(self, indexList):
        old_contained_rect = self.contained_rect
        for index in indexList:
            # if len(self.menu_items) > 1: #Original, always leaves one
            if len(self.menu_items) > 0:
                self.menu_items.pop(index)
        self.update_buttons = True
        return old_contained_rect

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
        if button.is_image == False:
            r = self.font.render
            width = button.rect[2]
            height = button.rect[3]
            rect = pygame.Rect(button.offset, (width, height))

            selected_image = pygame.Surface((width, height), -1)
            selected_image.blit(self.background, (0, 0), rect)
            text_image = r(button.text, True, self._selected_color)
            selected_image.blit(text_image, (0, 0))

            unselected_image = pygame.Surface((width, height), -1)
            unselected_image.blit(self.background, (0, 0), rect)
            text_image = r(button.text, True, self._unselected_color)
            unselected_image.blit(text_image, (0, 0))

        # Else this button is a graphic button, so create the selected and
        # unselected images based on the image provided
        else:
            orig_width, orig_height = button['b_image'].get_size()
            new_width = button.rect[2]
            new_height = button.rect[3]
            offset = (
                self.image_highlight_offset, self.image_highlight_offset)

            selected_image = pygame.Surface((new_width, new_height), -1)
            selected_image.fill(self.image_highlight_color)
            rect = pygame.Rect((button['offset'][0] + offset[0],
                                button['offset'][1] + offset[1]),
                               (orig_width, orig_height))
            selected_image.blit(self.background, offset, rect)
            selected_image.blit(button['b_image'], offset)

            unselected_image = pygame.Surface((new_width, new_height), -1)
            rect = pygame.Rect(button['offset'], (new_width, new_height))
            unselected_image.blit(self.background, (0, 0), rect)
            unselected_image.blit(button['b_image'], offset)

        button.s_image = selected_image
        button.u_image = unselected_image

    def position_buttons(self):
        max_width = 0
        max_height = 0
        counter = 0
        x_loc = 0
        y_loc = 0

        # Get the maximum width and height of the surfaces
        for button in self.menu_items:
            width = button.rect[2]
            height = button.rect[3]
            max_width = max(width, max_width)
            max_height = max(height, max_height)

        # Position the button in relation to each other
        for button in self.menu_items:
            # Find the offsets for the alignment of the buttons (left, center, or  right
            # Vertical Alignment
            offset_height = (max_height - button.rect[3]) / 2

            # Horizontal Alignment
            if self.alignment['horizontal'] == 'left':
                offset_width = 0
            elif self.alignment['horizontal'] == 'center':
                offset_width = (max_width - button.rect[2]) / 2
            elif self.alignment['horizontal'] == 'right':
                offset_width = (max_width - button.rect[2])
            else:
                offset_width = 0
                print("WARNING:  cMenu.position_buttons:  Horizontal "
                      "Alignment (value: %s) not recognized!  Left alignment "
                      "will be used % self.alignment['horizontal']")

            # Move the button location slightly based on the alignment offsets
            x_loc += offset_width
            y_loc += offset_height

            # Assign the location of the button
            button.offset = (x_loc, y_loc)
            x_loc -= offset_width
            y_loc -= offset_height
            y_loc += max_height
            counter += 1
            if counter == self.wrap_length:
                counter = 0
                x_loc += max_width
                y_loc = 0

        # Find the smallest Rect that will contain all of the buttons
        self.contained_rect = self.menu_items[0].rect.move(button.offset)
        for button in self.menu_items:
            temp_rect = button.rect.move(button.offset)
            self.contained_rect.union_ip(temp_rect)

        # Move the buttons to make them centered
        for button in self.menu_items:
            shift_x = 0 - (self.draw_surface.get_rect()[2] - button.rect[2]) / 2
            shift_y = 0 - (self.draw_surface.get_rect()[3] - button.rect[3]) / 2

            button.offset = (- shift_x, button.offset[1] - shift_y)

        # Re-find the smallest Rect that will contain all of the buttons
        self.contained_rect = self.menu_items[0].rect.move(button.offset)
        for button in self.menu_items:
            temp_rect = button.rect.move(button.offset)
            self.contained_rect.union_ip(temp_rect)

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
            else:
                return c_state

        else:
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

    def destroy_everything(self):
        while len(self.menu_items) > 0:
            self.remove_buttons([len(self.menu_items) - 1])
        self.draw_buttons(pygame.Rect((0, 0), self.draw_surface.get_size()))

    def receive_input(self, curr_input: user_input.Input):
        self.selected_button.receive_input(curr_input)

    def select_up(self):
        """Moves to the selection one higher, or loops to the bottom"""
        self.update((self.selection - 1) % len(self.menu_items))

    def select_down(self):
        """Moves to the selection one lower, or loops to the top"""
        self.update((self.selection + 1) % len(self.menu_items))


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
        pass


class SelectionButton(Button):
    def __init__(self, menu, button_list: typing.List[Button]):
        Button.__init__(self, menu, None, None)
        self.button_list = button_list
        self.selection = 0

    @property
    def selected_button(self):
        return self.button_list[self.selection]

    @property
    def text(self):
        return self.selected_button.text

    @property
    def confirm(self):
        return self.selected_button.confirm

    def receive_input(self, curr_input: user_input.Input):
        if isinstance(curr_input, user_input.Confirm):
            self.confirm()

        elif isinstance(curr_input, user_input.Up):
            self.menu.select_up()

        elif isinstance(curr_input, user_input.Down):
            self.menu.select_down()

        elif isinstance(curr_input, user_input.Left):
            self.left_choose_option()

        elif isinstance(curr_input, user_input.Right):
            self.right_choose_option()

    def left_choose_option(self):
        self.selection = (self.selection - 1) % len(self.button_list)
        self.menu.rewrite_buttons()

    def right_choose_option(self):
        self.selection = (self.selection + 1) % len(self.button_list)
        self.menu.rewrite_buttons()


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


class ConnectionScreen(screens.GameScreen):
    def __init__(self, display, session):
        screens.GameScreen.__init__(self, display, session)
        self.content = ArmySelectMenu(display, session)
        self.name = "Connection Screen"

    def execute_tick(self):
        self.content.draw_buttons()

    def _receive_input(self, curr_input: user_input.Input):
        self.content.receive_input(curr_input)
