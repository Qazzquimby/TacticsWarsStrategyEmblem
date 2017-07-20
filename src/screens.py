import abc

import user_input
from graphics import Display
from session import Session


class GameScreen(abc.ABC):
    def __init__(self, display: Display, session: Session):
        self.display = display  # type: Display
        self.session = session  # type: Session
        self.name = None  # type: str
        self.content = None

    def receive_input(self, curr_input: user_input.Input):
        print("Sending {} to {}".format(curr_input.name, self.name))
        self._receive_input(curr_input)

    def execute_tick(self):
        raise NotImplementedError

    def _receive_input(self, curr_input: user_input.Input):
        raise NotImplementedError


class ScreenEngine(object):
    def __init__(self, display, session, initial_screen):
        self._screen_stack = []
        self.display = display  # type: Display
        self.session = session  # type: Session
        self.main_game_screen = initial_screen  # type: GameScreen

        self.push_screen(self.main_game_screen)

    @property
    def screen(self) -> GameScreen:
        if len(self._screen_stack) < 1:
            self.push_screen(self.main_game_screen)
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

    def quit_game(self):
        self.session.quit_game()
