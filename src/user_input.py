import typing

import pygame

"""Classes related to receiving and interpreting user input"""

KEY_UP = 1
KEY_DOWN = 2


class Input(object):
    def __init__(self, name: str, priority: int):
        self.name = name  # type: str
        self.priority = priority  # type: int

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        try:
            return self.priority == other.priority and self.name == other.name
        except AttributeError:
            return False

    def __hash__(self):
        return hash(repr(self))


QUIT = Input("quit", 0)
CONFIRM = Input("confirm", 1)
BACK = Input("back", 2)
LEFT = Input("left", 3)
UP = Input("up", 3)
RIGHT = Input("right", 3)
DOWN = Input("down", 3)

STOP_LEFT = Input("left lift", 4)
STOP_UP = Input("up lift", 4)
STOP_RIGHT = Input("right lift", 4)
STOP_DOWN = Input("down lift", 4)

HELD_INPUTS = [LEFT, UP, RIGHT, DOWN]
HELD_INPUT_LIFTS = [STOP_LEFT, STOP_UP, STOP_RIGHT, STOP_DOWN]


class InputInterpreter(object):
    """Handles converting all key changes to a single action"""

    def __init__(self):
        self.control_map = ControlMap()
        self.held_keys = []

    def interpret_input(self) -> typing.Optional[Input]:
        """Returns the action to be performed this frame.

        Looks at this frame's key presses, maps them to their inputs,
        then returns the one with the lowest priority."""

        inputs, lifts = self._get_inputs()

        self.process_lifts(lifts)
        curr_input = self.process_inputs(inputs)
        self.process_lifts(lifts)
        return curr_input

    def _get_inputs(self) -> typing.List[Input]:
        """Maps this frame's key presses and lifts to their Inputs"""
        inputs = []
        lifts = []
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                curr_input = self.control_map.key_to_input((pygame.key.name(event.key), KEY_DOWN))
                if curr_input:
                    inputs.append(curr_input)

            elif event.type == pygame.KEYUP:
                curr_input = self.control_map.key_to_input((pygame.key.name(event.key), KEY_UP))
                if curr_input:
                    lifts.append(curr_input)

        return inputs, lifts

    def process_lifts(self, lifts):
        for lift in lifts:
            assert lift in HELD_INPUT_LIFTS
            print("lift", lift.name)
            if self.lift_action_to_push_action(lift) in self.held_keys:
                print("LIFTED")
                self.held_keys.remove(lift)

    def lift_action_to_push_action(self, lift):
        lifted = HELD_INPUTS[HELD_INPUT_LIFTS.index(lift)]
        return lifted

    def process_inputs(self, inputs):
        if inputs:
            priority_input = min(inputs)
            if priority_input in HELD_INPUTS:
                self.held_keys.append(priority_input)
                self.held_keys = list(set(self.held_keys))

            print([curr_input.name for curr_input in inputs], priority_input, self.held_keys)
            return priority_input
        else:
            try:
                return self.held_keys[-1]
            except IndexError:
                return None


class ControlMap(object):
    """Contains the mapping of key presses to Inputs."""

    def __init__(self):
        """_input_dict maps ("keyname", isKeyUp) to an Input"""

        self._input_dict = {
            ("x", KEY_DOWN): CONFIRM,
            ("z", KEY_DOWN): BACK,
            ("q", KEY_DOWN): QUIT,
            ("left", KEY_DOWN): LEFT,
            ("up", KEY_DOWN): UP,
            ("right", KEY_DOWN): RIGHT,
            ("down", KEY_DOWN): DOWN,

            ("left", KEY_UP): STOP_LEFT,
            ("up", KEY_UP): STOP_UP,
            ("right", KEY_UP): STOP_RIGHT,
            ("down", KEY_UP): STOP_DOWN,

        }

    def key_to_input(self, key: (str, int)) -> typing.Optional[typing.Type[Input]]:
        """Returns the Input mapped to the keypress"""
        try:
            return self._input_dict[key]
        except KeyError:
            return None
