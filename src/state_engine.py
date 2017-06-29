import main_game_screen


class StateEngine(object):
    def __init__(self, display, session):
        self._screen_stack = []
        self.display = display
        self.session = session
        self.main_game_screen = None  # Initialized by setup_initial_screen

        self.setup_initial_screen()

    def setup_initial_screen(self):
        self.main_game_screen = main_game_screen.MainGameScreen(self.display, self.session)

        self.push_screen()

    def get_screen(self):
        if len(self._screen_stack) < 1:
            self.setup_initial_screen()
            self.quit_game()
        return self._screen_stack[len(self._screen_stack) - 1]

    def push_screen(self):
        pass

    def pop_screen(self):
        pass

    def switch_screen(self):
        pass

    def receive_input(self, current_input):
        if current_input:
            self.get_screen().receive_input(current_input)

    def execute_tick(self, current_input):
        self.receive_input(current_input)
        # self.screen.execute_tick()

    def quit_game(self):
        self.session.quit_game()
