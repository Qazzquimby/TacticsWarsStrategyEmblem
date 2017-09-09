import abc
import typing

import pygame

"""Classes related to receiving and interpreting user input"""

KEY_UP = 1
KEY_DOWN = 2


class Input(abc.ABC):
    _PRIORITY = None  # type: int
    name = None  # type: str

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority

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
            return min(inputs)  # input with lowest priority #todo fix with static classes
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
                inputs.append(curr_input)

        return inputs


class ControlMap(object):
    """Contains the mapping of key presses to Inputs."""

    def __init__(self):
        """_input_dict maps ("keyname", isKeyUp) to an Input"""

        self._input_dict = {
            ("x", 2): Confirm,
            ("z", 2): Back,
            ("q", 2): Quit,
            ("left", 2): Left,
            ("up", 2): Up,
            ("right", 2): Right,
            ("down", 2): Down,
        }

    def key_to_input(self, key: (str, int)) -> typing.Optional[typing.Type[Input]]:
        """Returns the Input mapped to the keypress"""
        try:
            return self._input_dict[key]
        except KeyError:
            return None


class Quit(Input):
    _PRIORITY = 0
    name = "quit"

    @property
    def priority(self):
        return self._PRIORITY


class Confirm(Input):
    _PRIORITY = 1
    name = "confirm"

    @property
    def priority(self):
        return self._PRIORITY


class Back(Input):
    _PRIORITY = 2
    name = "back"

    @property
    def priority(self):
        return self._PRIORITY


class Left(Input):
    _PRIORITY = 3
    name = "left"

    @property
    def priority(self):
        return self._PRIORITY


class Up(Input):
    _PRIORITY = 4
    name = "up"

    @property
    def priority(self):
        return self._PRIORITY


class Right(Input):
    _PRIORITY = 5
    name = "right"

    @property
    def priority(self):
        return self._PRIORITY


class Down(Input):
    _PRIORITY = 6
    name = "down"

    @property
    def priority(self):
        return self._PRIORITY
