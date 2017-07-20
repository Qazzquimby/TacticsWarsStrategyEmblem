import pygame
import typing

import graphics
import point


class SpriteAnimation(object):
    def __init__(self, sprite_location: str, file_name: str):
        self.sprite_sheet = SpriteSheet(sprite_location, file_name)
        self.sprite_list = self.sprite_sheet.sprite_list  # type: list

    @property
    def sprite(self) -> pygame.Surface:
        return self.sprite_list[0]  # todo add animation


class SpriteSheet(object):
    def __init__(self, sprite_location: str, file_name: str):
        self.surface = self._load_sprite_sheet(sprite_location, file_name)  # type: pygame.Surface
        self.sheet_tile_width = self._get_tile_width()  # type: int
        self.sheet_tile_height = self._get_tile_height()  # type: int
        self._trim_sprite_sheet()
        self._sprite_list = self._make_sprite_list()  # type: typing.List[pygame.Surface]

    @property
    def sprite_list(self) -> typing.List[pygame.Surface]:
        return self._sprite_list

    def _load_sprite_sheet(self, sprite_location: str, file_name: str):
        converted_file_name = "../" + sprite_location + file_name + ".png"
        return pygame.image.load(converted_file_name).convert()

    def _get_tile_height(self) -> int:
        pixel_height = self.surface.get_height()
        tile_height = int(pixel_height / graphics.TILE_SIZE)
        return tile_height

    def _get_tile_width(self) -> int:
        pixel_width = self.surface.get_width()
        tile_width = int(pixel_width / graphics.TILE_SIZE)
        return tile_width

    def _trim_sprite_sheet(self):
        self._trim_width()
        self._trim_height()
        new_sheet = pygame.Surface((self.sheet_tile_width * graphics.TILE_SIZE,
                                    self.sheet_tile_height * graphics.TILE_SIZE))
        new_sheet.blit(self.surface, (0, 0))
        self.surface = new_sheet

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
                screen_pixel = point.PixelPoint(tile_x * graphics.TILE_SIZE + pixel_x,
                                                tile_y * graphics.TILE_SIZE + pixel_y)
                if not self._is_pixel_empty(screen_pixel):
                    is_empty = False
                    break
        return is_empty

    def _is_pixel_empty(self, pixel_point: point.PixelPoint) -> bool:
        sprite_color = self.surface.get_at((pixel_point.x, pixel_point.y))
        is_empty = sprite_color == (255, 255, 255)
        return is_empty

    def _make_sprite_list(self):
        sprite_list = []
        for tile_x in range(self.sheet_tile_width):
            sprite = pygame.Surface((graphics.TILE_SIZE, graphics.TILE_SIZE))
            rect_of_sheet = pygame.Rect((tile_x * graphics.TILE_SIZE, 0),
                                        (graphics.TILE_SIZE, graphics.TILE_SIZE))
            sprite.blit(self.surface, (0, 0), rect_of_sheet)
            sprite_list.append(sprite)
        return sprite_list


class MissingSpriteException(Exception):
    pass

class DrawNullEntityException(Exception):
    pass