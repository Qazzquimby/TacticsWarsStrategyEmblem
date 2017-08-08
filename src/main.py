import sys

import pygame

import graphics
import menus
import screens
import session
import user_input


# fixme patching over missing army select


class Clock(object):
    def __init__(self):
        self.FPS = 30
        self.pygame_clock = pygame.time.Clock()

    def wait_for_next_tick(self):
        self.pygame_clock.tick(self.ms_per_frame)


    @property
    def ms_per_frame(self):
        return int(1000 / self.FPS)


class Main(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tactics Wars Strategy Emblem")

        self.session = session.Session()  # type: session.Session
        self.display = graphics.Display()  # type: graphics.Display
        self.state_engine = screens.ScreenEngine(
            self.display, self.session, self.setup_initial_screen())  # type:screens.ScreenEngine

        self.clock = Clock()

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
        # fixme mockup
        # world_setup = WorldSetup()
        # army_importer = armymod.ArmyImporter()
        # world_setup.add_player(IronLegion())
        # world_setup.add_player(army_importer.plugins[0])
        # return world_screen.MainGameScreen(self.display, self.session, world_setup)

        return menus.ConnectionScreen(self.display, self.session)

    def uninit(self):
        self.quit_game()

    def quit_game(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main = Main()
