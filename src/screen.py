import abc
import display
import session
import user_input


class GameScreen(abc.ABC):
    def __init__(self, display, session):
        """Abstract class for displays in the game
        @type display: src.display.Display
        @param display:
            Display object for surface and execute_tick reference.

        @type settings: src.settings.Settings
        @param settings:
            src.settings.Settings. the instance of the settings object

        @type session: src.session.Session

        name:
            str.  the name of the screen
        content:
            
        __receive_input:
            Internal function that may be set for use with menus.
        """
        self.display = display  # type: display.Display
        self.session = session  # type: session.Session
        self.name = None  # type: str
        self.content = None
        self.__receive_input = None

    def receive_input(self, curr_input: user_input.Input):
        print("Sending {} to {}".format(curr_input.name, self.name))
        self.__receive_input(curr_input)
