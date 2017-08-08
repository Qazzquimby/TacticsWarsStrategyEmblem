import abc
import typing

import pygame

"""Classes related to receiving and interpreting user input"""

KEY_UP = 1
KEY_DOWN = 2


class Input(abc.ABC):
    _PRIORITY = None  # type: int
    name = None  # type: str

    def __init__(self):
        pass

    def __lt__(self, other):
        return self.priority < other.priority

    @property
    def priority(self) -> int:
        return self._PRIORITY


class InputInterpreter(object):
    """Handles converting all key changes to a single action"""

    def __init__(self):
        self.control_map = ControlMap()

    def interpret_input(self) -> typing.Optional[Input]:
        """Returns the action to be performed this frame.

        Looks at this frame's key presses, maps them to their inputs,
        then returns the one with the lowest priority."""

        inputs = self._get_inputs()
        if inputs:
            return min(inputs)  # input with lowest priority
        else:
            return None

    def _get_inputs(self) -> typing.List[Input]:
        """Maps this frame's key presses to their Inputs"""
        inputs = []
        for event in pygame.event.get():
            curr_input = None
            if event.type == pygame.KEYDOWN:
                curr_input = self.control_map.key_to_input((pygame.key.name(event.key), KEY_DOWN))
            elif event.type == pygame.KEYUP:
                curr_input = self.control_map.key_to_input((pygame.key.name(event.key), KEY_UP))

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

    def key_to_input(self, key: (str, int)) -> typing.Optional[typing.Type[Input]]:
        """Returns the Input mapped to the keypress"""
        try:
            return self._input_dict[key]
        except KeyError:
            return None


class Confirm(Input):
    _PRIORITY = 1
    name = "confirm"

    def __init__(self):
        Input.__init__(self)

    @property
    def priority(self):
        return self._PRIORITY


class Back(Input):
    _PRIORITY = 2
    name = "back"

    def __init__(self):
        Input.__init__(self)

    @property
    def priority(self):
        return self._PRIORITY


class Left(Input):
    _PRIORITY = 3
    name = "left"

    def __init__(self):
        Input.__init__(self)

    @property
    def priority(self):
        return self._PRIORITY


class Up(Input):
    _PRIORITY = 4
    name = "up"

    def __init__(self):
        Input.__init__(self)

    @property
    def priority(self):
        return self._PRIORITY


class Right(Input):
    _PRIORITY = 5
    name = "right"

    def __init__(self):
        Input.__init__(self)

    @property
    def priority(self):
        return self._PRIORITY


class Down(Input):
    _PRIORITY = 6
    name = "down"

    def __init__(self):
        Input.__init__(self)

    @property
    def priority(self):
        return self._PRIORITY
