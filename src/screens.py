import abc

# Type checking
import graphics
import sessionmod
import user_input


class ScreenEngine(object):
    def __init__(self, display: graphics.Display, session: sessionmod.Session):
        self._screen_stack = []
        self.display = display  # type: graphics.Display
        self.session = session  # type: sessionmod.Session

    @property
    def screen(self) -> "GameScreen":
        if len(self._screen_stack) == 0:
            self.quit_game()
            # self.push_screen(EmptyScreen())
            return EmptyScreen()
        return self._screen_stack[len(self._screen_stack) - 1]

    def push_screen(self, screen: "GameScreen"):
        if len(self._screen_stack) > 0:
            self.screen.exit()
        self._screen_stack.append(screen)
        self.screen.enter()

    def pop_screen(self):
        self.screen.exit()
        try:
            self._screen_stack.pop(len(self._screen_stack) - 1)
        except IndexError:
            pass
        self.screen.enter()

    def switch_screen(self, screen: "GameScreen"):
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


class GameScreen(abc.ABC):
    def __init__(self, screen_engine: ScreenEngine):
        self.screen_engine = screen_engine
        self.display = screen_engine.display  # type: graphics.Display
        self.session = screen_engine.session  # type: sessionmod.Session
        self.name = NotImplemented  # type: str
        self.content = NotImplemented

    def receive_input(self, curr_input: user_input.Input):
        print("Sending {} to {}".format(curr_input.name, self.name))
        self._receive_input(curr_input)

    def execute_tick(self):
        raise NotImplementedError

    def _receive_input(self, curr_input: user_input.Input):
        raise NotImplementedError

    def enter(self):
        pass

    def exit(self):
        pass


class EmptyScreen(GameScreen):
    def __init__(self):
        # Initialized before screen_engine, so does not run GameScreen.__init__ which requires it.
        pass

    def execute_tick(self):
        pass

    def _receive_input(self, curr_input: user_input.Input):
        pass
