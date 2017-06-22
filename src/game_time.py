import pygame


class Clock(object):
    def __init__(self):
        self.FPS = 30
        self.pygame_clock = pygame.time.Clock()

    def wait_for_next_tick(self):
        self.pygame_clock.tick()
