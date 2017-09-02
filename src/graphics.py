import typing

import pygame

import points

TILE_SIZE = 32

SCREEN_TILE_WIDTH = 30
SCREEN_TILE_HEIGHT = 20
SCREEN_SIZE_POINT = points.ScreenPoint.from_tile(SCREEN_TILE_WIDTH, SCREEN_TILE_HEIGHT)

SCREEN_WIDTH = SCREEN_SIZE_POINT.pixel_x
SCREEN_HEIGHT = SCREEN_SIZE_POINT.pixel_y

TOP_BAR_DRAW_POINT = points.ScreenPoint(0, 0)
TOP_BAR_TILE_HEIGHT = 2
TOP_BAR_TILE_SIZE_POINT = points.ScreenPoint.from_tile(SCREEN_TILE_WIDTH, TOP_BAR_TILE_HEIGHT)
TOP_BAR_HEIGHT = TOP_BAR_TILE_SIZE_POINT.pixel_y

MENU_TILE_HEIGHT = 5
MENU_DRAW_POINT = points.ScreenPoint.from_tile(0, SCREEN_TILE_HEIGHT - MENU_TILE_HEIGHT)
MENU_SIZE_POINT = points.ScreenPoint.from_tile(SCREEN_TILE_WIDTH, MENU_TILE_HEIGHT)
MENU_HEIGHT = MENU_SIZE_POINT.pixel_y

MAP_TILE_HEIGHT = SCREEN_TILE_HEIGHT - TOP_BAR_TILE_HEIGHT - MENU_TILE_HEIGHT
MAP_DRAW_POINT = points.ScreenPoint.from_tile(0, TOP_BAR_TILE_HEIGHT)
MAP_SIZE_POINT = points.ScreenPoint.from_tile(SCREEN_TILE_WIDTH, MAP_TILE_HEIGHT)
MAP_HEIGHT = MAP_SIZE_POINT.pixel_y

MAP_TILE_WIDTH = MAP_SIZE_POINT.tile_x
MAP_WIDTH = MAP_SIZE_POINT.pixel_x

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
TRANSPARENT = (255, 000, 255)
ANIMATION_FRAME_LENGTH = 15


class Display(object):
    def __init__(self):
        self.display_size_multiplier = 1.5

        self._display_width = int(SCREEN_WIDTH * self.display_size_multiplier)
        self._display_height = int(SCREEN_HEIGHT * self.display_size_multiplier)

        self._surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._display = pygame.display.set_mode((self._display_width, self._display_height))
        self._surface.convert()

    @property
    def display(self) -> pygame.display:
        return self._display

    @property
    def surface(self) -> pygame.Surface:
        return self._surface

    def flip_display(self):
        self._display.blit(
            pygame.transform.scale(
                self._surface, (self._display_width, self._display_height)),
            (0, 0))
        pygame.display.flip()

    def execute_tick(self):
        self.flip_display()

    def blit(self, surface: pygame.Surface, dest: typing.Union[points.ScreenPoint, tuple]):
        if isinstance(dest, points.ScreenPoint):
            dest = dest.pixel
        self._surface.blit(surface, dest)


def make_surface(dimensions: tuple):
    surface = pygame.Surface(dimensions)
    surface.convert()
    surface.set_colorkey((255, 0, 255))
    return surface


def make_invisible_surface(dimensions: tuple):
    """Creates a transparent alpha make_surface."""
    surface = make_surface(dimensions)
    surface.fill((255, 0, 255))
    return surface
