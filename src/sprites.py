import random
import typing

import pygame

import graphics
import points


class SpriteAnimation(object):
    def __init__(self,
                 sprite_location: str,
                 file_name: str,
                 animation_frame_length: typing.Optional[int] = None):

        self.animation_frame_length = animation_frame_length
        if self.animation_frame_length is None:
            self.animation_frame_length = graphics.ANIMATION_FRAME_LENGTH  # type: int

        self.sprite_sheet = SpriteSheet(sprite_location, file_name)
        self.sprite_list = self.sprite_sheet.sprite_list  # type: list
        self._current_sprite_index = random.randrange(0, len(self.sprite_list) - 1)
        self._time_spent_at_index = random.randrange(0, graphics.ANIMATION_FRAME_LENGTH - 1)

    @property
    def sprite(self) -> pygame.Surface:
        sprite = self.sprite_list[self._current_sprite_index]
        self._animate()
        return sprite

    def _animate(self):
        self._increment_time_spent()
        self._update_sprite_index()

    def _increment_time_spent(self):
        try:
            self._time_spent_at_index = (
                                            self._time_spent_at_index + 1) % self.animation_frame_length
        except ZeroDivisionError:
            raise ValueError("sprite animation given frame length of 0")

    def _update_sprite_index(self):
        if self._time_spent_at_index == 0:
            self._current_sprite_index = (self._current_sprite_index + 1) % len(self.sprite_list)


class SpriteSheet(object):
    def __init__(self, sprite_location: str, file_name: str):
        self.original_sprite_sheet_surface = self._load_sprite_sheet(sprite_location,
                                                                     file_name)  # type: pygame.Surface
        self.sheet_tile_width = self._get_tile_width()  # type: int
        self.sheet_tile_height = self._get_tile_height()  # type: int
        self._trim_sprite_sheet()
        self._sprite_list = self._make_sprite_list()  # type: typing.List[pygame.Surface]

    @property
    def sprite_list(self) -> typing.List[pygame.Surface]:
        return self._sprite_list

    def _load_sprite_sheet(self, sprite_location: str, file_name: str):
        converted_file_name = "../" + sprite_location + file_name + ".png"
        sprite_sheet = pygame.image.load(converted_file_name).convert()  # type: pygame.Surface
        sprite_sheet.set_colorkey((255, 0, 255), pygame.RLEACCEL)
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
    pass


class DrawNullEntityException(Exception):
    pass
