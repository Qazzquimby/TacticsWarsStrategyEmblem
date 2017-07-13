import world_screen
from screen import GameScreen
from world_setup import WorldSetup
import user_input
import ironlegion
from display import Display
from session import Session


class StateEngine(object):
    def __init__(self, display, session):
        self._screen_stack = []
        self.display = display  # type: Display
        self.session = session  # type: Session
        self.main_game_screen = self.setup_initial_screen()  # type: GameScreen

        self.push_screen(self.main_game_screen)

    @property
    def screen(self) -> GameScreen:
        if len(self._screen_stack) < 1:
            self.setup_initial_screen()
            self.quit_game()
        return self._screen_stack[len(self._screen_stack) - 1]

    def push_screen(self, screen: GameScreen):
        self._screen_stack.append(screen)

    def pop_screen(self):
        self._screen_stack.pop(len(self._screen_stack) - 1)

    def switch_screen(self, screen: GameScreen):
        self.pop_screen()
        self.push_screen(screen)

    def receive_input(self, current_input: user_input.Input):
        if current_input:
            self.screen.receive_input(current_input)

    def execute_tick(self, current_input: user_input.Input):
        self.receive_input(current_input)
        self.screen.execute_tick()

    def setup_initial_screen(self):

        world_setup = WorldSetup()

        # fixme mockup
        world_setup.add_player(ironlegion.IronLegion())

        return world_screen.MainGameScreen(self.display, self.session, world_setup)

    def quit_game(self):
        self.session.quit_game()
