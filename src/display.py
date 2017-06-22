# import win32api
import pygame


class Display(object):
    def __init__(self):
        self.screen_width = 960
        self.screen_height = 640

        self.display_width = 960  # win32api.GetSystemMetrics(0)
        self.display_height = 640  # win32api.GetSystemMetrics(1)

        self.surface = pygame.Surface((self.screen_width,
                                       self.screen_height))
        self.display = pygame.display.set_mode((self.display_width,
                                                self.display_height))

    def flip_display(self):
        self.display.blit(
            pygame.transform.scale(
                self.surface, (self.display_width, self.display_height)),
            (0, 0))
        pygame.display.flip()

    def execute_tick(self):
        self.flip_display()

    def update_rects(self, rect_list):
        """Updates only the area signified by the rect_list"""
        pygame.display.update(rect_list)
