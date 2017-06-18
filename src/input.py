import pygame
import abc

"""Classes related to receiving and interpreting user input"""

KEY_UP = 1
KEY_DOWN = 2


class Input(abc.ABC):
    def __init__(self):
        self._PRIORITY = None
        self.name = None

    def __lt__(self, other):
        return self.priority <  other.priority

    @property
    def priority(self):
        return self._PRIORITY


class Confirm(Input):
    def __init__(self):
        Input.__init__(self)
        self._PRIORITY = 1
        self.name = "confirm"

    @property
    def priority(self):
        return self._PRIORITY


class Back(Input):
    def __init__(self):
        Input.__init__(self)
        self._PRIORITY = 2
        self.name = "back"

    @property
    def priority(self):
        return self._PRIORITY


class Left(Input):
    def __init__(self):
        Input.__init__(self)
        self._PRIORITY = 3
        self.name = "left"

    @property
    def priority(self):
        return self._PRIORITY


class Up(Input):
    def __init__(self):
        Input.__init__(self)
        self._PRIORITY = 4
        self.name = "up"

    @property
    def priority(self):
        return self._PRIORITY


class Right(Input):
    def __init__(self):
        Input.__init__(self)
        self._PRIORITY = 5
        self.name = "right"

    @property
    def priority(self):
        return self._PRIORITY


class Down(Input):
    def __init__(self):
        Input.__init__(self)
        self._PRIORITY = 6
        self.name = "down"

    @property
    def priority(self):
        return self._PRIORITY


class InputInterpreter(object):
    """Handles converting all key changes to a single action"""

    def __init__(self):
        self.control_map = ControlMap()

    def interpret_input(self) -> Input:
        """Returns the action to be performed this frame.

        Looks at this frame's key presses, maps them to their inputs,
        then returns the one with the lowest priority."""

        inputs = self._get_inputs()
        if inputs:
            return min(inputs)  # input with lowest priority
        else:
            return None

    def _get_inputs(self) -> Input:
        """Maps this frame's key presses to their Inputs"""
        inputs = []
        for event in pygame.event.get():
            curr_input = None
            if event.type == pygame.KEYDOWN:
                curr_input = self.control_map.get_input((
                    pygame.key.name(event.key),
                    KEY_DOWN))
            elif event.type == pygame.KEYUP:
                curr_input = self.control_map.get_input((
                    pygame.key.name(event.key),
                    KEY_UP))

            if callable(curr_input):
                inputs.append(curr_input())

        return inputs


class ControlMap(object):
    """Contains the mapping of key presses to Inputs."""

    def __init__(self):
        """_input_dict maps ("keyname", isKeyUp) to an Input"""

        self._input_dict = {
            ("x", True): Confirm,
            ("z", True): Back,
            ("left", True): Left,
            ("up", True): Up,
            ("right", True): Right,
            ("down", True): Down,
        }

    def get_input(self, key: (str, int)) -> Input:
        """Returns the Input mapped to the keypress"""
        try:
            return self._input_dict[key]
        except KeyError:
            return None
