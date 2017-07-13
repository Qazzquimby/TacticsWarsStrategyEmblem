import sys

import pygame

import display
import state_engine
import user_input
import session
import game_time


class Main(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tactics Wars Strategy Emblem")

        self.session = session.Session()  # type: session.Session
        self.display = display.Display()  # type: display.Display
        self.state_engine = state_engine.StateEngine(self.display,
                                                     self.session)  # type: state_engine.StateEngine
        self.clock = game_time.Clock()  # type: game_time.Clock
        self.input_interpreter = user_input.InputInterpreter()  # type: user_input.InputInterpreter

        self.game_loop()
        self.uninit()

    def game_loop(self):
        while self.session.get_game_running():
            self.execute_tick()

    def execute_tick(self):
        current_input = self.input_interpreter.interpret_input()
        self.state_engine.execute_tick(current_input)
        self.display.execute_tick()
        self.clock.wait_for_next_tick()

    def uninit(self):
        self.quit_game()

    def quit_game(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main = Main()
