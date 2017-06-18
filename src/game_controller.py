import src.input
import src.menus


class GameController(object):
    def __init__(self, display, settings, session):
        self.input_interpreter = src.input.InputInterpreter()
        self.screen = src.menus.ConnectionScreen(display, settings, session)

    def receive_input(self):
        curr_input = self.input_interpreter.interpret_input()
        if curr_input:
            self.screen.receive_input(curr_input)

    def update(self, clock):
        self.screen.update(clock)
