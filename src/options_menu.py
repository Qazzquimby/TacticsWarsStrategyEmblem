#! /usr/bin/python

# noinspection

## \file  content.py
#  \brief General Menu Class
#  \author Scott Barlow
#  \date 2009
#  \version 1.0.3
#
#  This is a content class written for pygame/Python.  The content is designed to work
#  with a program using a finite state machine (but it could also be easily
#  modified to have the 'buttons' return functions).  The content 'buttons' contain
#  a 'state' (a state could really be anything you want) and this 'state' is
#  what is returned when the user selects/presses the button.  The program
#  controlling the content can then act on this returned state as required.  This
#  helps to write non-blocking code.
#
#  The content can have text buttons, image buttons (that get highlighted on all
#  sides to detect which is selected), or any combination of the two.
#
#  The content is flexible and can be dynamically changed.  The 'buttons' will
#  auto-magically execute_tick themselves the next time they are drawn to the screen
#  (via the execute_tick method, which calls the draw method).  The draw method should
#  not be called itself.  'Buttons' can be added or removed at any time.
#
#  The content can be positioned by the top left corner (a rectangle containing all
#  buttons is what gets moved).  It can be changed to center the entire content
#  (i.e. center that containing rectangle) on that same position coordinate.  Or
#  the user can center the entire content on the self.draw_surface.  Note that if
#  the pygame screen is given to the content, then the entire window will be
#  available to be drawn to.  But if the user gives the content another pygame
#  surface, then that surface itself will need to be blitted to the pygame
#  screen at some point.  Furthermore, the user can align the buttons to align
#  on the left, tobe centerd, or to align themselves on the right.  Also, they
#  can be aligned vertically on the top, center, or bottom.
#
#  The user can dynamically change the colors of the font/highlights, the
#  padding between buttons (left/right and top/bottom), the thickness of the
#  highlight around image buttons, and the orientation of the content (if the
#  'buttons' will be stacked top to bottom ('vertical') or left to right
#  ('horizontal').
#
#  The best way to figure out the content is to tinker around with it.  Run the
#  example programs, change attributes, and play with the content.
#
#
#       Copyright 2009 Scott Barlow
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA or see <http://www.gnu.org/licenses/>.
#
#
#  Changelog
#     V1.0.0 - Initial Release
#     V1.0.1 - Added get_current_image method
#     V1.0.2 - Fixed a bug in the set_font method (to execute_tick the rect of the
#              text buttons when the font is changed
#     V1.0.3 - Added self.refresh_whole_surface_on_load functionality
#


# -------------------------------------------------------------------------------
# ---[ Imports
# ]-----------------------------------------------------------------
# -------------------------------------------------------------------------------
import pygame

# -------------------------------------------------------------------------------
# ---[ Defines
# ]-----------------------------------------------------------------
# -------------------------------------------------------------------------------
# RGB color for Black
BLACK = (0, 0, 0)

# RGB color for White
WHITE = (255, 255, 255)

# RGB color for Red
RED = (255, 0, 0)

# RGB color for Green
GREEN = (0, 255, 0)

# RGB color for Blue
BLUE = (0, 0, 255)

# This is a user event that should be sent whenever the game state is changed
#  (at the main game loop level)
EVENT_CHANGE_STATE = pygame.USEREVENT + 1


# -------------------------------------------------------------------------------
# ---[ cMenu Class
# ]-------------------------------------------------------------
# -------------------------------------------------------------------------------
## This class is used to display and control a content
#
class cOptionsMenu:
    ## ---[ __init__
    # ]-----------------------------------------------------------
    #  @param   self        The class itself, Python standard
    #  @param   x           The x location to shift the buttons by when the
    #                       button is drawn to the surface in the execute_tick method
    #  @param   y           The y location to shift the buttons by when the
    #                       button is drawn to the surface in the execute_tick method
    #  @param   h_pad       Number the extra pixels to pad the buttons by (on
    #  the
    #                       left/right)
    #  @param   v_pad       Number the extra pixels to pad the buttons by (on
    #  the
    #                       top/bottom).
    #  @param   orientation Should be 'vertical' or 'horizontal'.  The buttons
    #                       will be put vertically or horizontally until
    # 'number'
    #                       (the next argument) of buttons have been created at
    #                       which point it will start a new row or column
    #  @param   number      The number of buttons to put vertically or
    #                       horizontally before starting a new row or column
    #  @param   background  The background to use for the buttons (what will
    # show
    #                       up behind the buttons).  This is often the
    #                       surface that they will be blitted to via the execute_tick
    #                       method
    #  @param   buttonList  This is a list of buttons to be added (though
    #                       more buttons can be added via another method).  The
    #                       elements of the list should be tuples of 3 parts as
    #                       shown: ('text', state, image) where text is the text
    #                       that will be shown for the button, state is what
    # will
    #                       be returned when the button is pressed (enter is
    #                       hit), and image is None if the button is just going
    #                       to display text, or else is an image itself if the
    #                       button will be displayed as an image instead of
    # text.
    #
    #  Initialize the class


    def __init__(self, x, y, h_pad, v_pad, orientation, number, background,
                 buttonList):
        ## content items
        self.menu_items = []  # List of content items
        self.font = pygame.font.Font(None, 32)  # Font to use

        self.x = x  # Top left corner (of surface)
        self.y = y  # relative to the screen/window
        self.change_number = number  # See description above
        self.orientation = orientation  # See description above
        self.horizontal_padding = h_pad  # See description above
        self.vertical_padding = v_pad  # See description above

        self.selection = 0  # The currently selected button
        self.u_color = WHITE  # Color for unselected text
        self.s_color = RED  # Color for selected text
        self.image_highlight_color = BLUE  # Color for the image highlights
        self.image_highlight_offset = 2  # Addition padding around image
        # buttons only for the highlight

        self.background = background.copy()  # The unedited background image
        self.draw_surface = background  # Surface to draw to
        self.centered = False  # True if the content is centered
        self.centeredOnScreen = False  # True if the content is centered
        self.update_buttons = True  # True if the positions of the
        # buttons need to be updated
        self.refresh_whole_surface_on_load = False  # When the content is first
        # displayed (when the event
        # EVENT_CHANGE_STATE is given to
        # the execute_tick method), the entire
        # self.draw_surface will be
        # updated

        # This dictionary contains the alignment orientation of the buttons
        # related to each other.  It shifts the button within the bounds of
        # 'max_width' and 'max_height' in the self.position_buttons() method.
        self.alignment = {'vertical': 'top',
                          'horizontal': 'left'}

        # Now add any buttons that were sent in
        self.add_buttons(buttonList)

    ## ---[ redraw_all
    # ]---------------------------------------------------------
    def redraw_all(self):
        for button in self.menu_items:
            button['redraw'] = True

    ## ---[ get_current_text
    # ]---------------------------------------------------
    def get_current_text(self):
        return self.menu_items[self.selection]['text']

    ## ---[ get_current_image
    # ]--------------------------------------------------
    def get_current_image(self):
        return self.menu_items[self.selection]['b_image']

    ## ---[ set_unselected_color
    # ]-----------------------------------------------
    def set_unselected_color(self, new_color):
        self.u_color = new_color
        self.update_buttons = True

    ## ---[ set_selected_color
    # ]-------------------------------------------------
    def set_selected_color(self, new_color):
        self.s_color = new_color
        self.update_buttons = True

    ## ---[ set_image_highlight_color
    # ]------------------------------------------
    def set_image_highlight_color(self, new_color):
        self.image_highlight_color = new_color
        self.update_buttons = True

    ## ---[ set_image_highlight_thickness
    # ]--------------------------------------
    def set_image_highlight_thickness(self, new_thick):
        old_th = self.image_highlight_offset
        # We need to execute_tick the width of the button images now (the images
        # themselves will be updated before the next refresh/re-draw).  Note
        # that
        # we only change the rect on the image buttons since we only
        # highlight the
        # image buttons (not the text buttons)
        for button in self.menu_items:
            if button['b_image'] is not None:
                button['rect'][2] = button['rect'][2] - 2 * old_th + 2 * new_thick
                button['rect'][3] = button['rect'][3] - 2 * old_th + 2 * new_thick
        self.image_highlight_offset = new_thick
        self.update_buttons = True

    ## ---[ set_padding
    # ]--------------------------------------------------------
    def set_padding(self, h_pad, v_pad):
        self.horizontal_padding = h_pad
        self.vertical_padding = v_pad
        self.update_buttons = True

    ## ---[ set_orientation
    # ]----------------------------------------------------
    def set_orientation(self, new_orientation):
        if new_orientation == 'vertical' or new_orientation == 'horizontal':
            self.orientation = new_orientation
            self.update_buttons = True
        else:
            print
            'WARNING:  cMenu.set_orientation:  Invalid argument ' \
            'new_orientation (value: %d)' % new_orientation

    ## ---[ set_change_number
    # ]--------------------------------------------------
    def set_change_number(self, new_change_number):
        self.change_number = new_change_number
        self.update_buttons = True

    ## ---[ set_refresh_whole_screen_on_load
    # ]-----------------------------------
    def set_refresh_whole_surface_on_load(self, new_val=True):
        self.refresh_whole_surface_on_load = new_val  # Should be True or False

    ## ---[ set_font
    # ]-----------------------------------------------------------
    def set_font(self, font):
        self.font = font

        # We need to execute_tick the width and height of the text buttons since we
        # calculated their width and height based on the font
        for button in self.menu_items:
            if button['b_image'] is None:
                width, height = self.font.size(button['text'])
                button['rect'][2] = width
                button['rect'][3] = height

        self.update_buttons = True

    ## ---[ set_alignment
    # ]------------------------------------------------------
    #  @param   self     The class itself, Python standard
    #  @param   v_align  The way to align the text vertically within its 'cell'
    #  @param   h_align  The way to align the text horizontally within its
    # 'cell'
    #
    #  This method sets the alignment of the buttons within their 'cell' (
    # i.e. it
    #  sets the alignment of the button (based on it's width and height) within
    #  the max_width and max_height values calculated in the
    #  self.position_buttons() method).  The self.position_buttons() method is
    #  also where the alignment occurs.  The valid alignments are:
    #     left
    #     center
    #     right
    #
    def set_alignment(self, v_align, h_align):
        if v_align in ['top', 'center', 'bottom']:
            self.alignment['vertical'] = v_align
        if h_align in ['left', 'center', 'right']:
            self.alignment['horizontal'] = h_align
        self.update_buttons = True

    ## ---[ set_position
    # ]-------------------------------------------------------
    #  @param   self   The class itself, Python standard
    #  @param   x      The x (horizontal location)
    #  @param   y      The y (vertical location)
    #
    #  This method sets the x and y locations for the content.  By default, this
    #  sets the position of the content with respect to the top left corner of the
    #  self.draw_surface.  If 'centered' is true, then this is the location of
    #  the center of the content.
    #
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.update_buttons = True

    ## ---[ set_center
    # ]---------------------------------------------------------
    #  @param   self           The class itself, Python standard
    #  @param   centered       A boolean, centers the content if it is True,
    # default
    #                          value is True
    #  @param   centeredOnScreen  If this is true, then the content will be
    # centered
    #                             on the entire self.draw_surface surface.
    #
    #  When passed a value of True, this centers the content at the self.x and
    #  self.y locations.  If False is passed to it, then this makes the top left
    #  corner of the content start at the x and y location with respect to the
    #  self.draw_surface.  If centerScreen is True, then self.centered is set to
    #  true, regardless of the value passed in
    #
    def set_center(self, centered, centeredOnScreen):
        if centeredOnScreen:
            self.centeredOnScreen = centeredOnScreen
            self.centered = False
        else:
            self.centeredOnScreen = False
            self.centered = centered
        self.update_buttons = True

    ## ---[ add_buttons
    # ]--------------------------------------------------------
    #  @param   self         The class itself, Python standard
    #  @param   buttonList   List of content buttons to be added
    #
    #  Used to add button(s) to the content
    #
    def add_buttons(self, buttonList):
        for button in buttonList:
            self.menu_items.append(self.create_button(button))
        self.update_buttons = True

    ## ---[ remove_buttons
    # ]-----------------------------------------------------
    #  @param   self         The class itself, Python standard
    #  @param   indexList    List of indexes to be removed
    #
    #  Used to remove button(s) from the content
    #
    def remove_buttons(self, indexList):
        old_contained_rect = self.contained_rect
        for index in indexList:
            # if len(self.menu_items) > 1: #Original, always leaves one
            if len(self.menu_items) > 0:
                self.menu_items.pop(index)
        self.update_buttons = True
        return old_contained_rect

    ## ---[ update_button_locations
    # ]--------------------------------------------
    #  @param   self         The class itself, Python standard
    #
    #  This method is just used to execute_tick the location of the buttons when the
    #  a change is made
    #
    def update_button_locations(self):
        if len(self.menu_items) > 0:
            self.position_buttons()
        self.set_button_images()
        self.update_buttons = False

    ## ---[ create_button
    # ]------------------------------------------------------
    #  @param   self         The class itself, Python standard
    #  @param   button_info  A list with the button text, the next state to
    #                        return, and the image (if applicable)
    #
    #  Create the button dictionary for a new button.  Note that this button is
    #  useless until the set_button_images method is called which is where the
    #  button images are created and assigned.  The reason it is not done here
    #  is because we need to know the location of the button on the background
    #  which is not assigned until position_buttons() is called.  Since position
    #  buttons depends on the width and height of each button, we just calculate
    #  those here, then we set the location of the buttons via the
    #  position_buttons() method, then we make the actual images via the
    #  set_button_images() function
    #
    def create_button(self, button_info):
        # If this button is not an image, set the width and height based on the
        # text
        if button_info[2] is None:
            width, height = self.font.size(button_info[0])
            button_rect = pygame.Rect((0, 0), (width, height))
        # Else this button is a graphic button, so create the width and height
        # based on the image provided
        else:
            width, height = button_info[2].get_size()
            offset = (self.image_highlight_offset, self.image_highlight_offset)
            new_width = width + 2 * offset[0]  # Make room for the highlight on
            new_height = height + 2 * offset[1]  # all sides
            button_rect = pygame.Rect((0, 0), (new_width, new_height))

        set_redraw = True  # When the button is created, it needs to be drawn
        set_selected = False  # When the button is created, it is not selected

        new_button = {'text': button_info[0],
                      'state': button_info[1],
                      'selected': set_selected,
                      'rect': button_rect,
                      'offset': (0, 0),
                      'redraw': set_redraw,
                      'b_image': button_info[2],  # base image
                      's_image': None,  # image when selected and not
                      'u_image': None}  # selected (created in
        # set_button_images)

        return new_button

        # def set_button_text(self, buttonIndex, newText):

    ## ---[ set_button_images
    # ]--------------------------------------------------
    #  @param   self         The class itself, Python standard
    #
    #  Create the button images to be displayed - adjusted for the location of
    #  the button over the background image
    #
    def set_button_images(self):
        for button in self.menu_items:
            # If this button is not an image, create the selected and unselected
            # images based on the text
            if button['b_image'] is None:
                r = self.font.render
                width = button['rect'][2]
                height = button['rect'][3]
                rect = pygame.Rect(button['offset'], (width, height))

                # For each of the text button (selected and unselected),
                # create a
                # surface of the required size (already calculated before), blit
                # the background image to the surface, then render the text
                # and blit
                # that text onto the same surface.
                selected_image = pygame.Surface((width, height), -1)
                selected_image.blit(self.background, (0, 0), rect)
                text_image = r(button['text'], True, self.s_color)
                selected_image.blit(text_image, (0, 0))

                unselected_image = pygame.Surface((width, height), -1)
                unselected_image.blit(self.background, (0, 0), rect)
                text_image = r(button['text'], True, self.u_color)
                unselected_image.blit(text_image, (0, 0))

            # Else this button is a graphic button, so create the selected and
            # unselected images based on the image provided
            else:
                orig_width, orig_height = button['b_image'].get_size()
                new_width = button['rect'][2]
                new_height = button['rect'][3]
                offset = (
                    self.image_highlight_offset, self.image_highlight_offset)

                # Selected image!
                # --------------------------------------------------
                # Create the surface, fill the surface with the highlight color,
                # then blit the background image to the surface (inside of the
                # highlight area), and then blit the actual button base image
                #  over
                # the background
                selected_image = pygame.Surface((new_width, new_height), -1)
                selected_image.fill(self.image_highlight_color)
                rect = pygame.Rect((button['offset'][0] + offset[0],
                                    button['offset'][1] + offset[1]),
                                   (orig_width, orig_height))
                selected_image.blit(self.background, offset, rect)
                selected_image.blit(button['b_image'], offset)

                # Unselected image!
                # ------------------------------------------------
                # Create the surface, blit the background image onto the
                # surface (to
                # make sure effects go away when the button is no longer
                # selected),
                # and then blit the actual button base image over the background
                unselected_image = pygame.Surface((new_width, new_height), -1)
                rect = pygame.Rect(button['offset'], (new_width, new_height))
                unselected_image.blit(self.background, (0, 0), rect)
                unselected_image.blit(button['b_image'], offset)

            button['s_image'] = selected_image
            button['u_image'] = unselected_image

    ## ---[ position_buttons
    # ]---------------------------------------------------
    #  @param   self    The class itself, Python standard
    #
    #  Sets the positions for the buttons
    #
    def position_buttons(self):
        width = 0
        height = 0
        max_width = 0
        max_height = 0
        counter = 0
        x_loc = self.x
        y_loc = self.y

        # Get the maximum width and height of the surfaces
        for button in self.menu_items:
            width = button['rect'][2]
            height = button['rect'][3]
            max_width = max(width, max_width)
            max_height = max(height, max_height)

        # Position the button in relation to each other
        for button in self.menu_items:
            # Find the offsets for the alignment of the buttons (left,
            # center, or
            # right
            # Vertical Alignment
            if self.alignment['vertical'] == 'top':
                offset_height = 0
            elif self.alignment['vertical'] == 'center':
                offset_height = (max_height - button['rect'][3]) / 2
            elif self.alignment['vertical'] == 'bottom':
                offset_height = (max_height - button['rect'][3])
            else:
                offset_height = 0
                print('WARNING:  cMenu.position_buttons:  Vertical Alignment ' \
                      '(value: %s) not recognized!  Left alignment will be '
                      'used' \
                      %
                      self.alignment['vertical'])

            # Horizontal Alignment
            if self.alignment['horizontal'] == 'left':
                offset_width = 0
            elif self.alignment['horizontal'] == 'center':
                offset_width = (max_width - button['rect'][2]) / 2
            elif self.alignment['horizontal'] == 'right':
                offset_width = (max_width - button['rect'][2])
            else:
                offset_width = 0
                print("WARNING:  cMenu.position_buttons:  Horizontal "
                      "Alignment (value: %s) not recognized!  Left alignment "
                      "will be used % self.alignment['horizontal']")
            # # Horizontal Alignment
            # if self.alignment['horizontal'] == 'left':
            # 	offset_width = 0
            # elif self.alignment['horizontal'] == 'center':
            # 	offset_width = (max_width - button['rect'][2])/2
            # elif self.alignment['horizontal'] == 'right':
            # 	offset_width = (max_width - button['rect'][2])
            # else:
            # 	offset_width = 0
            # 	print 'WARNING:  cMenu.position_buttons:  Horizontal
            # Alignment '\
            # 			'(value: %s) not recognized!  Left alignment will be
            # used'\
            # 													  %
            # self.alignment['horizontal']



            # Move the button location slightly based on the alignment offsets
            x_loc += offset_width
            y_loc += offset_height

            # Assign the location of the button
            button['offset'] = (x_loc, y_loc)

            # Take the alignment offsets away after the button position has been
            # assigned so that the new button can start fresh again
            x_loc -= offset_width
            y_loc -= offset_height

            # Add the width/height to the position based on the orientation
            # of the
            # content.  Add in the padding.
            if self.orientation == 'vertical':
                y_loc += max_height + self.vertical_padding
            else:
                x_loc += max_width + self.horizontal_padding
            counter += 1

            # If we have reached the self.change_number of buttons, then it
            # is time
            # to start a new row or column
            if counter == self.change_number:
                counter = 0
                if self.orientation == 'vertical':
                    x_loc += max_width + self.horizontal_padding
                    y_loc = self.y
                else:
                    y_loc += max_height + self.vertical_padding
                    x_loc = self.x

        # Find the smallest Rect that will contain all of the buttons
        self.contained_rect = self.menu_items[0]['rect'].move(button['offset'])
        for button in self.menu_items:
            temp_rect = button['rect'].move(button['offset'])
            self.contained_rect.union_ip(temp_rect)

        # We shift the buttons around on the screen if they are supposed to be
        # centered (on the surface itself or at (x, y).  We do it here
        # instead of
        # at the beginning of this function because we need to know what the
        # self.contained_rect is to know the correct amount to shift them.
        if self.centeredOnScreen:
            shift_x = self.x - (self.draw_surface.get_rect()[2] -
                                self.contained_rect[2]) / 2
            shift_y = self.y - (self.draw_surface.get_rect()[3] -
                                self.contained_rect[3]) / 2
        elif self.centered:
            shift_x = (self.contained_rect[2]) / 2
            shift_y = (self.contained_rect[3]) / 2
        if self.centeredOnScreen or self.centered:
            # Move the buttons to make them centered
            for button in self.menu_items:
                button['offset'] = (button['offset'][0] - shift_x,
                                    button['offset'][1] - shift_y)

            # Re-find the smallest Rect that will contain all of the buttons
            self.contained_rect = self.menu_items[0]['rect'].move(
                button['offset'])
            for button in self.menu_items:
                temp_rect = button['rect'].move(button['offset'])
                self.contained_rect.union_ip(temp_rect)

    ## ---[ execute_tick
    # ]-------------------------------------------------------------
    #  @param   self      The class itself, Python standard
    #  @param   e         The last event
    #  @param   c_state   The current state of the game from where this is
    # called
    #  @return            A list of rectangles of where the screen changed
    #  @return            The new state for the game
    #
    #  Update the content surface, redraw it to the stored surface
    # self.draw_surface
    #
    def update(self, c_state=-1):
        # redraw_full_menu = False

        # setting to true just to make errors more easy to notice.
        # Plus I don't see it ever being an issue.
        redraw_full_menu = True

        self.selection_prev = self.selection

        self.selection = c_state

        o = self.orientation
        n = self.change_number

        # Should be the first transition when the content is made, and sets up
        # the content
        if c_state == -1:

            c_state = 0  # default button (starts at topmost button)
            self.selection = 0

            self.menu_items[self.selection_prev]['selected'] = False
            self.menu_items[self.selection]['selected'] = True
            self.redraw_all()
            rectangle_list = self.draw_buttons()
            if self.refresh_whole_surface_on_load:
                rectangle_list = pygame.Rect((0, 0),
                                             self.draw_surface.get_size())
                return [rectangle_list], c_state
            else:
                return [self.contained_rect], c_state

        elif redraw_full_menu:
            self.menu_items[self.selection_prev]['selected'] = False
            self.menu_items[self.selection]['selected'] = True
            self.redraw_all()
            rectangle_list = self.draw_buttons(
                pygame.Rect((0, 0), self.draw_surface.get_size()))
            return rectangle_list, c_state

        elif self.selection != self.selection_prev:
            self.menu_items[self.selection_prev]['selected'] = False
            self.menu_items[self.selection]['selected'] = True
            rectangle_list = self.draw_buttons()
            return rectangle_list, c_state

        # If no updates were made, return defaults
        return [None], c_state

    ## ---[ draw_buttons
    # ]-------------------------------------------------------
    #  @param   self          The class itself, Python standard
    #  @param   redraw_rect   If this pygame.Rect is provided, then the entire
    #                         background will be drawn to the surface in the
    # area
    #                         of this rect before the buttons are drawn
    #  @return                A list of rectangles of where the screen changed
    #
    #  Draw the buttons to the self.draw_surface and return a list of Rect's
    # that
    #  indicate where on the surface changes were made
    #
    def draw_buttons(self, redraw_rect=None):
        rect_list = []

        # If buttons have been changed (added button(s), deleted button(s),
        # changed colors, etc, etc), then we need to execute_tick the button locations
        # and images
        if self.update_buttons:
            self.update_button_locations()

            # Print a warning if the buttons are partially/completely off the
            # surface
            if not self.draw_surface.get_rect().contains(self.contained_rect):
                print
                'WARNING:  cMenu.draw_buttons:  Some buttons are partially ' \
                'or completely off of the self.draw_surface!'

        # If a rect was provided, redraw the background surface to the area
        # of the
        # rect before we draw the buttons
        if redraw_rect is not None:
            offset = (redraw_rect[0], redraw_rect[1])
            drawn_rect = self.draw_surface.blit(self.background,
                                                offset,
                                                redraw_rect)
            rect_list.append(drawn_rect)

        # Cycle through the buttons, only draw the ones that need to be redrawn
        for button in self.menu_items:
            if button['redraw']:
                if button['selected']:
                    image = button['s_image']
                else:
                    image = button['u_image']

                drawn_rect = self.draw_surface.blit(image,
                                                    button['offset'],
                                                    button['rect'])
                rect_list.append(drawn_rect)

        return rect_list

    def destroy_everything(self):
        while len(self.menu_items) > 0:
            self.remove_buttons([len(self.menu_items) - 1])
        self.redraw_all()
        rectangle_list = self.draw_buttons(
            pygame.Rect((0, 0), self.draw_surface.get_size()))

    def select_up(self):
        """Moves to the selection one higher, or loops to the bottom"""
        self.update((self.selection - 1) % len(self.menu_items))

    def select_down(self):
        """Moves to the selection one lower, or loops to the top"""
        self.update((self.selection + 1) % len(self.menu_items))

# ---[ END OF FILE
# ]-------------------------------------------------------------
