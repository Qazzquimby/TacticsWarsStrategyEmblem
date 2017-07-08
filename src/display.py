# import win32api
import pygame
import size_constants


class Display(object):
    def __init__(self):
        self.display_size_multiplier = 1

        self._display_width = size_constants.SCREEN_WIDTH * self.display_size_multiplier
        # win32api.GetSystemMetrics(0)
        self._display_height = size_constants.SCREEN_HEIGHT * self.display_size_multiplier
        # win32api.GetSystemMetrics(1)

        self._surface = pygame.Surface((size_constants.SCREEN_WIDTH,
                                        size_constants.SCREEN_HEIGHT))

        self._display = pygame.display.set_mode((self._display_width,
                                                 self._display_height))

    def flip_display(self):
        self._display.blit(
            pygame.transform.scale(
                self._surface, (self._display_width, self._display_height)),
            (0, 0))
        pygame.display.flip()

    def execute_tick(self):
        self.flip_display()

    def update_rects(self, rect_list):
        """Updates only the area signified by the rect_list"""
        pygame.display.update(rect_list)

    def get_display(self):
        return self._display

    def blit(self, surface: pygame.Surface, dest):
        self._surface.blit(surface, dest)