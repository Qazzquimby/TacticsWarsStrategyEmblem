import sys
import pygame

import graphics
import screens
import user_input
import session

#fixme patching over missing army select
from world_setup import WorldSetup
import world_screen
import armymod

class Clock(object):
    def __init__(self):
        self.FPS = 30
        self.pygame_clock = pygame.time.Clock()

    def wait_for_next_tick(self):
        self.pygame_clock.tick()


class Main(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tactics Wars Strategy Emblem")

        self.session = session.Session()  # type: session.Session
        self.display = graphics.Display()  # type: graphics.Display
        self.state_engine = screens.ScreenEngine(self.display,
                                                 self.session,
                                                 self.setup_initial_screen())  # type:
        # screens.ScreenEngine
        self.clock = Clock()  # type: import main

        self.input_interpreter = user_input.InputInterpreter()  # type: user_input.InputInterpreter

        self.game_loop()
        self.uninit()

    def game_loop(self):
        while self.session.game_running:
            self.execute_tick()

    def execute_tick(self):
        current_input = self.input_interpreter.interpret_input()
        self.state_engine.execute_tick(current_input)
        self.display.execute_tick()
        self.clock.wait_for_next_tick()

    def setup_initial_screen(self):
        world_setup = WorldSetup()

        # fixme mockup
        army_importer = armymod.ArmyImporter()
        army_importer.print_plugins()
        # world_setup.add_player(IronLegion())
        world_setup.add_player(army_importer.plugins[0])

        return world_screen.MainGameScreen(self.display, self.session, world_setup)

    def uninit(self):
        self.quit_game()

    def quit_game(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main = Main()


