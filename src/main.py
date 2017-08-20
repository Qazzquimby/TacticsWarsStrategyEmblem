import sys

import pygame

import graphics
import menus
import screens
import sessionmod
import user_input

FPS = 30


class Clock(object):
    def __init__(self):
        self.pygame_clock = pygame.time.Clock()

    def wait_for_next_tick(self):
        self.pygame_clock.tick(self.ms_per_frame)

    @property
    def ms_per_frame(self):
        return int(1000 / FPS)


class Main(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tactics Wars Strategy Emblem")

        self.session = sessionmod.Session()  # type: sessionmod.Session
        self.display = graphics.Display()  # type: graphics.Display

        self.screen_engine = self.init_screen_engine()

        self.clock = Clock()
        self.input_interpreter = user_input.InputInterpreter()  # type: user_input.InputInterpreter

        self.run_game()

    def init_screen_engine(self):
        screen_engine = screens.ScreenEngine(self.display, self.session)
        initial_screen = menus.MapSelectScreen(screen_engine)
        screen_engine.push_screen(initial_screen)
        return screen_engine

    def run_game(self):
        self.game_loop()
        self.uninit()

    def game_loop(self):
        while self.session.game_running:
            self.execute_tick()

    def execute_tick(self):
        current_input = self.input_interpreter.interpret_input()
        self.screen_engine.execute_tick(current_input)
        self.display.execute_tick()
        self.clock.wait_for_next_tick()

    def uninit(self):
        self.quit_game()

    def quit_game(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    MAIN = Main()
