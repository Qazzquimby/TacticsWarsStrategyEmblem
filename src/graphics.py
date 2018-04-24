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

"""Core graphics functionality

This module holds display related constants and manages creating and updating the draw window.

Attributes:
    TILE_SIZE (int): The width and height of a tile in pixels. Tiles are always square.

    SCREEN_TILE_WIDTH (int): Width of the screen in tiles.
    SCREEN_TILE_HEIGHT (int): Height of the screen in tiles.
    SCREEN_SIZE_POINT (points.ScreenPoint): Bottom right point of screen.

    SCREEN_WIDTH (int): Width of the screen in pixels.
    SCREEN_HEIGHT (int): Height of the screen in pixels.

    TOP_BAR_DRAW_POINT (points.ScreenPoint): Top left point of the top bar.
    TOP_BAR_TILE_HEIGHT (int): Height of the top bar in tiles.
    TOP_BAR_TILE_SIZE_POINT (points.ScreenPoint): Bottom right point of the top bar.
    TOP_BAR_HEIGHT (int): Height of the top bar in pixels.

    MENU_TILE_HEIGHT (int): Height of menu in tiles.
    MENU_DRAW_POINT (points.ScreenPoint): Top left point of menu.
    MENU_SIZE_POINT (points.ScreenPoint): Bottom right point of the menu.
    MENU_HEIGHT (int): Height of menu in pixels.

    MAP_TILE_HEIGHT (int): Height of the map in tiles.
    MAP_DRAW_POINT (points.ScreenPoint): Top left corner of the map.
    MAP_SIZE_POINT (points.ScreenPoint): Bottom right corner of the map.
    MAP_HEIGHT (int): Height of map in pixels.

    MAP_TILE_WIDTH (int): Width of map in tiles.
    MAP_WIDTH (int): Width of map in pixels.

    RED (tuple(int)): The rgb color code representing red.
    WHITE (tuple(int)): The rgb color code representing white.
    BLACK (tuple(int)): The rgb color code representing black.
    TRANSPARENT (tuple(int)): The rgb color code representing transparency.

    DEFAULT_ANIMATION_FRAME_LENGTH (int): The length a frame should be shown in milliseconds before
    advancing in the animation, unless overwritten in the animation.
"""

import pygame

import points

TILE_SIZE = 32

SCREEN_TILE_WIDTH = 30
SCREEN_TILE_HEIGHT = 20
SCREEN_SIZE_POINT = points.point_from_tile(points.ScreenPoint, SCREEN_TILE_WIDTH,
                                           SCREEN_TILE_HEIGHT)

SCREEN_WIDTH = SCREEN_SIZE_POINT.pixel_x
SCREEN_HEIGHT = SCREEN_SIZE_POINT.pixel_y

TOP_BAR_DRAW_POINT = points.ScreenPoint(0, 0)
TOP_BAR_TILE_HEIGHT = 2
TOP_BAR_TILE_SIZE_POINT = points.point_from_tile(points.ScreenPoint, SCREEN_TILE_WIDTH,
                                                 TOP_BAR_TILE_HEIGHT)
TOP_BAR_HEIGHT = TOP_BAR_TILE_SIZE_POINT.pixel_y

MENU_TILE_HEIGHT = 5
MENU_DRAW_POINT = points.point_from_tile(points.ScreenPoint,
                                         0,
                                         SCREEN_TILE_HEIGHT - MENU_TILE_HEIGHT)
MENU_SIZE_POINT = points.point_from_tile(points.ScreenPoint, SCREEN_TILE_WIDTH, MENU_TILE_HEIGHT)
MENU_HEIGHT = MENU_SIZE_POINT.pixel_y

MAP_TILE_HEIGHT = SCREEN_TILE_HEIGHT - TOP_BAR_TILE_HEIGHT - MENU_TILE_HEIGHT
MAP_DRAW_POINT = points.point_from_tile(points.ScreenPoint, 0, TOP_BAR_TILE_HEIGHT)
MAP_SIZE_POINT = points.point_from_tile(points.ScreenPoint, SCREEN_TILE_WIDTH, MAP_TILE_HEIGHT)
MAP_HEIGHT = MAP_SIZE_POINT.pixel_y

MAP_TILE_WIDTH = MAP_SIZE_POINT.tile_x
MAP_WIDTH = MAP_SIZE_POINT.pixel_x

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT = (255, 0, 255)

DEFAULT_ANIMATION_FRAME_LENGTH = 15


class Display(object):
    """ Holds the screen surface and handles screen updates.

    Attributes:
        self.display_size_multiplier (float): Scales the size of the entire screen.
    """

    def __init__(self):
        self.display_size_multiplier = 1.5

        self._display_width = int(SCREEN_WIDTH * self.display_size_multiplier)
        self._display_height = int(SCREEN_HEIGHT * self.display_size_multiplier)

        # pylint: disable=too-many-function-args
        self._surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._display = pygame.display.set_mode((self._display_width, self._display_height))

        # noinspection PyArgumentList
        self._surface.convert()

    @property
    def display(self):
        """pygame.display: Gets the current window."""
        return self._display

    @property
    def surface(self):
        """pygame.Surface: Gets the surface being displayed."""
        return self._surface

    def flip_display(self):
        """Scales the surface to screen size and updates the screen with the surface contents."""
        self._display.blit(
            pygame.transform.scale(self._surface, (self._display_width, self._display_height)),
            (0, 0))

        pygame.display.flip()

    def execute_tick(self):
        """Called each tick. Updates the display based on the games' state."""
        self.flip_display()

    def blit(self, surface, destination):
        """ Draws the given surface onto the display's surface, with destination as as the top
        left point.

        Args:
            surface (pygame.Surface): The image to draw onto the display surface.
            destination (points.ScreenPoint or tuple): The point on the display surface to begin
            drawing.
        """
        if isinstance(destination, points.ScreenPoint):
            destination = destination.pixel
        self._surface.blit(surface, destination)


# noinspection PyArgumentList
def make_surface(dimensions):
    """Makes a new surface

    Args:
        dimensions (tuple): The x, y size of the surface in pixels.

    Returns:
        pygame.Surface: The created surface.
    """
    surface = pygame.Surface(dimensions)  # pylint: disable=too-many-function-args
    surface.convert()
    surface.set_colorkey(TRANSPARENT)
    return surface


def make_invisible_surface(dimensions: tuple):
    """Makes a new transparent surface

    Args:
        dimensions (tuple): The x, y size of the surface in pixels.

    Returns:
        pygame.Surface: The created surface.
    """
    surface = make_surface(dimensions)
    surface.fill(TRANSPARENT)
    return surface
