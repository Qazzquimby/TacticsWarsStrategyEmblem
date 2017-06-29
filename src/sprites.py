import pygame
import size_constants


class SpriteAnimation(object):
    def __init__(self, file_name):

        self.animation_sprite_sheet = self.load_sprite_sheet(file_name)
        self.find_animation_sprite_sheet_width()

    def load_sprite_sheet(self, file_name):
        try:
            return pygame.image.load(file_name).convert()
        except pygame.error:
            raise (pygame.error, "error loading sprite sheet", file_name)

    def find_animation_sprite_sheet_width(self):
        for row in self.animation_sprite_sheet:
            for tile in row:
                pass
