import sys

import pygame

import src.display
import src.game_controller
import src.input
import src.session
import src.settings


class Main(object):
    def __init__(self):
        """
        
        
        

        """
        pygame.init()
        pygame.display.set_caption("Tactics Wars Strategy Emblem")

        self.session = src.session.Session()
        self.settings = src.settings.Settings()
        self.display = src.display.Display()
        self.game_controller = src.game_controller.GameController(
            self.display, self.settings, self.session)

        self.clock = pygame.time.Clock()
        while not self.session.game_over:
            self.frame()
        self.quit_game()

    def frame(self):
        self.game_controller.receive_input()
        self.game_controller.update(self.clock)
        self.display.flip_display()
        self.clock.tick(self.settings.FPS)

    @staticmethod
    def quit_game():
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main = Main()
