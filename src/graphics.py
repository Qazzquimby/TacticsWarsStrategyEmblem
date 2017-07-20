# import win32api
import pygame
from point import Point


class Display(object):
    def __init__(self):
        self.display_size_multiplier = 1.5

        self._display_width = int(SCREEN_WIDTH * self.display_size_multiplier)
        # win32api.GetSystemMetrics(0)
        self._display_height = int(SCREEN_HEIGHT * self.display_size_multiplier)
        # win32api.GetSystemMetrics(1)

        self._surface = pygame.Surface((SCREEN_WIDTH,
                                        SCREEN_HEIGHT))

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

    @property
    def display(self) -> pygame.display:
        return self._display

    def blit(self, surface: pygame.Surface, dest_point: Point):
        dest = (dest_point.x, dest_point.y)
        self._surface.blit(surface, dest)


TILE_SIZE = 32
SCREEN_TILE_WIDTH = 30
SCREEN_WIDTH = TILE_SIZE * SCREEN_TILE_WIDTH
SCREEN_TILE_HEIGHT = 20
SCREEN_HEIGHT = TILE_SIZE * SCREEN_TILE_HEIGHT
TOP_BAR_TILE_HEIGHT = 2
TOP_BAR_HEIGHT = TILE_SIZE * TOP_BAR_TILE_HEIGHT
MENU_TILE_HEIGHT = 5
MENU_HEIGHT = TILE_SIZE * MENU_TILE_HEIGHT
MAP_TILE_HEIGHT = SCREEN_TILE_HEIGHT - TOP_BAR_TILE_HEIGHT - MENU_TILE_HEIGHT
MAP_HEIGHT = TILE_SIZE * MAP_TILE_HEIGHT
MAP_TILE_WIDTH = SCREEN_TILE_WIDTH
MAP_WIDTH = TILE_SIZE * MAP_TILE_WIDTH
BLACK = (0, 0, 0)
