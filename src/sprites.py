import pygame
import size_constants


class SpriteAnimation(object):
    def __init__(self, file_name):

        self.sprite_sheet = self.load_sprite_sheet(file_name)
        self.sheet_tile_width = self.get_tile_width()
        self.sheet_tile_height = self.get_tile_height()
        self.trim_sprite_sheet()

    def load_sprite_sheet(self, file_name):
        converted_file_name = "../sprites/" + file_name
        return pygame.image.load(converted_file_name).convert()

    def trim_sprite_sheet(self):
        self.trim_width()
        self.trim_height()
        new_sheet = pygame.Surface((self.sheet_tile_width * size_constants.TILE_SIZE,
                                    self.sheet_tile_height * size_constants.TILE_SIZE))
        new_sheet.blit(self.sprite_sheet, (0, 0))
        self.sprite_sheet = new_sheet

    def trim_width(self):
        for tile_x in range(self.get_tile_width()):
            if self.is_column_empty(tile_x):
                self.sheet_tile_width = tile_x
                break

    def trim_height(self):
        for tile_y in range(self.get_tile_height()):
            if self.is_row_empty(tile_y):
                self.sheet_tile_height = tile_y
                break

    def is_column_empty(self, tile_x):
        is_empty = True
        for tile_y in range(self.sheet_tile_height):
            if not self.is_tile_empty(tile_x, tile_y):
                is_empty = False
                break
        return is_empty

    def is_row_empty(self, tile_y):
        is_empty = True
        for tile_x in range(self.sheet_tile_width):
            if not self.is_tile_empty(tile_x, tile_y):
                is_empty = False
                break
        return is_empty

    def is_tile_empty(self, tile_x, tile_y):
        is_empty = True
        for pixel_y in range(size_constants.TILE_SIZE):
            for pixel_x in range(size_constants.TILE_SIZE):
                absolute_pixel_x = tile_x * size_constants.TILE_SIZE + pixel_x
                absolute_pixel_y = tile_y * size_constants.TILE_SIZE + pixel_y
                if not self.is_pixel_empty(absolute_pixel_x, absolute_pixel_y):
                    is_empty = False
                    break
        return is_empty

    def is_pixel_empty(self, x, y):
        sprite_color = self.sprite_sheet.get_at((x, y))
        is_empty = sprite_color == (255, 255, 255)
        return is_empty

    def get_tile_height(self):
        pixel_height = self.sprite_sheet.get_height()
        tile_height = int(pixel_height / size_constants.TILE_SIZE)
        return tile_height

    def get_tile_width(self):
        pixel_width = self.sprite_sheet.get_width()
        tile_width = int(pixel_width / size_constants.TILE_SIZE)
        return tile_width


