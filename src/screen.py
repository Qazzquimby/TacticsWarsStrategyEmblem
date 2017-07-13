import abc
from display import Display
from session import Session
import user_input


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
