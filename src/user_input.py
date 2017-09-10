import typing

import pygame

"""Classes related to receiving and interpreting user input"""

KEY_UP = 1
KEY_DOWN = 2


class Input(object):
    def __init__(self, name: str, priority: int):
        self.name = name  # type: str
        self.priority = priority  # type: int

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority


QUIT = Input("quit", 0)
CONFIRM = Input("confirm", 1)
BACK = Input("back", 2)
LEFT = Input("left", 3)
UP = Input("up", 4)
RIGHT = Input("right", 5)
DOWN = Input("down", 6)


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

            if curr_input is not None:
                inputs.append(curr_input)

        return inputs


class ControlMap(object):
    """Contains the mapping of key presses to Inputs."""

    def __init__(self):
        """_input_dict maps ("keyname", isKeyUp) to an Input"""

        self._input_dict = {
            ("x", 2): CONFIRM,
            ("z", 2): BACK,
            ("q", 2): QUIT,
            ("left", 2): LEFT,
            ("up", 2): UP,
            ("right", 2): RIGHT,
            ("down", 2): DOWN,
        }

    def key_to_input(self, key: (str, int)) -> typing.Optional[typing.Type[Input]]:
        """Returns the Input mapped to the keypress"""
        try:
            return self._input_dict[key]
        except KeyError:
            return None
