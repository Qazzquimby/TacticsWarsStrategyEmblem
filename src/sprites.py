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

"""Classes related to images and animation."""

import random
import typing

import pygame

import graphics
import points


class SpriteAnimation(object):
    """A wrapper on a series of sprites and optional timing values to allow looping animation.

    Attributes:
        self.animation_frame_length (int): The number of frames for which each sprite in the
        animation will be displayed.
        self.sprite_sheet (SpriteSheet): A sprite sheet object holding the sprites to animate.
        self.sprite_list (list(pygame.Surface)): A list of the sprites in the sprite sheet.
    """

    def __init__(self, sprite_location, file_name, animation_frame_length=None):

        self.animation_frame_length = animation_frame_length
        if self.animation_frame_length is None:
            self.animation_frame_length = graphics.DEFAULT_ANIMATION_FRAME_LENGTH  # type: int

        self.sprite_sheet = SpriteSheet(sprite_location, file_name)
        self.sprite_list = self.sprite_sheet.sprite_list  # type: list

        try:
            self._current_sprite_index = random.randrange(0, len(self.sprite_list) - 1)
        except ValueError:
            self._current_sprite_index = 0

        self._time_spent_at_index = random.randrange(0, self.animation_frame_length - 1)

    @property
    def sprite(self):
        """pygame.Surface: The current sprite to display."""
        sprite = self.sprite_list[self._current_sprite_index]
        self._animate()
        return sprite

    def _animate(self):
        self._increment_time_spent()
        self._update_sprite_index()

    def _increment_time_spent(self):
        try:
            next_time_at_index = self._time_spent_at_index + 1
            self._time_spent_at_index = next_time_at_index % self.animation_frame_length
        except ZeroDivisionError:
            raise ValueError("sprite animation given frame length of 0")

    def _update_sprite_index(self):
        if self._time_spent_at_index == 0:
            self._current_sprite_index = (self._current_sprite_index + 1) % len(self.sprite_list)


class SpriteSheet(object):
    """A surface containing sprites to be animated.

    Attributes:
        self.original_sprite_sheet_surface (pygame.Surface): The original image the sprites are
        pulled from.
        self.sheet_tile_width (int): The width of the sprite sheet in tiles.
        self.sheet_tile_height (int): The height of the sprite sheet in tiles.
    """

    def __init__(self, sprite_location, file_name):
        self.original_sprite_sheet_surface = self._load_sprite_sheet(sprite_location,
                                                                     file_name)
        self.sheet_tile_width = self._get_tile_width()
        self.sheet_tile_height = self._get_tile_height()
        self._trim_sprite_sheet()
        self._sprite_list = self._make_sprite_list()

    @property
    def sprite_list(self) -> typing.List[pygame.Surface]:
        """List[pygame.Surface]: The sprites, in animation order."""
        return self._sprite_list

    @staticmethod
    def _load_sprite_sheet(sprite_location: str, file_name: str):
        converted_file_name = "../" + sprite_location + file_name + ".png"
        sprite_sheet = pygame.image.load(converted_file_name).convert()  # type: pygame.Surface
        sprite_sheet.set_colorkey((255, 0, 255), pygame.RLEACCEL)  # pylint: disable=no-member
        return sprite_sheet

    def _get_tile_height(self) -> int:
        pixel_height = self.original_sprite_sheet_surface.get_height()
        tile_height = int(pixel_height / graphics.TILE_SIZE)
        return tile_height

    def _get_tile_width(self) -> int:
        pixel_width = self.original_sprite_sheet_surface.get_width()
        tile_width = int(pixel_width / graphics.TILE_SIZE)
        return tile_width

    def _trim_sprite_sheet(self):
        self._trim_width()
        self._trim_height()
        new_sheet = graphics.make_invisible_surface((self.sheet_tile_width * graphics.TILE_SIZE,
                                                     self.sheet_tile_height * graphics.TILE_SIZE))
        new_sheet.blit(self.original_sprite_sheet_surface, (0, 0))
        self.original_sprite_sheet_surface = new_sheet

    def _trim_width(self):
        for tile_x in range(self._get_tile_width()):
            if self._is_column_empty(tile_x):
                self.sheet_tile_width = tile_x
                break

    def _trim_height(self):
        for tile_y in range(self._get_tile_height()):
            if self._is_row_empty(tile_y):
                self.sheet_tile_height = tile_y
                break

    def _is_column_empty(self, tile_x: int) -> bool:
        is_empty = True
        for tile_y in range(self.sheet_tile_height):
            if not self._is_tile_empty(tile_x, tile_y):
                is_empty = False
                break
        return is_empty

    def _is_row_empty(self, tile_y: int) -> bool:
        is_empty = True
        for tile_x in range(self.sheet_tile_width):
            if not self._is_tile_empty(tile_x, tile_y):
                is_empty = False
                break
        return is_empty

    def _is_tile_empty(self, tile_x: int, tile_y: int) -> bool:
        is_empty = True
        for pixel_y in range(graphics.TILE_SIZE):
            for pixel_x in range(graphics.TILE_SIZE):
                screen_pixel = points.ScreenPoint(tile_x * graphics.TILE_SIZE + pixel_x,
                                                  tile_y * graphics.TILE_SIZE + pixel_y)
                if not self._is_pixel_empty(screen_pixel):
                    is_empty = False
                    break
        return is_empty

    def _is_pixel_empty(self, point: points.ScreenPoint) -> bool:
        sprite_color = self.original_sprite_sheet_surface.get_at(point.pixel)
        is_empty = sprite_color == graphics.TRANSPARENT
        return is_empty

    def _make_sprite_list(self):
        sprite_list = []
        for tile_x in range(self.sheet_tile_width):
            tile_size = (graphics.TILE_SIZE, graphics.TILE_SIZE)
            sprite = graphics.make_invisible_surface(tile_size)

            tile_rect = pygame.Rect((tile_x * graphics.TILE_SIZE, 0), tile_size)
            sprite.blit(self.original_sprite_sheet_surface, (0, 0), tile_rect)
            sprite_list.append(sprite)
        return sprite_list


class MissingSpriteException(Exception):
    """Thrown when a sprite is requested that does not exist."""
    pass


class DrawNullEntityException(Exception):
    """Thrown when a Null Entity is drawn."""
    pass
