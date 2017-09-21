import typing
from collections import OrderedDict

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
        self.input_repeater = InputRepeater(self)

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
            push_action = self.lift_action_to_push_action(lift)
            if push_action in self.held_keys:
                print("LIFTED")
                self.held_keys.remove(push_action)

    def lift_action_to_push_action(self, lift):
        lifted = HELD_INPUTS[HELD_INPUT_LIFTS.index(lift)]
        return lifted

    def process_inputs(self, inputs):
        if inputs:
            return self._process_new_inputs(inputs)
        else:
            if self.held_key:
                return self._held_key_input()
            else:
                self.input_repeater.held_key = None
                return None

    def _process_new_inputs(self, inputs):
        priority_input = min(inputs)
        if priority_input in HELD_INPUTS:
            self._hold_key(priority_input)
        return priority_input

    def _hold_key(self, key):
        self.held_keys.append(key)
        self.held_keys = list(OrderedDict.fromkeys(self.held_keys))  # deduplicate

    @property
    def held_key(self):
        try:
            return self.held_keys[-1]
        except IndexError:
            return None

    def _held_key_input(self):
        # todo improve cursor movement
        return self.input_repeater.input


class InputRepeater(object):
    def __init__(self, input_interpreter: InputInterpreter):
        self.input_interpreter = input_interpreter
        self.current_hold_time = 0
        self.hold_time_before_roll = 8
        self.held_key = None

    @property
    def input(self):
        if self.input_interpreter.held_key == self.held_key:
            print(self.current_hold_time)
            if self.current_hold_time < self.hold_time_before_roll:
                self.current_hold_time += 1
                return None
            else:
                return self.roll()
        else:
            self.held_key = self.input_interpreter.held_key
            self.current_hold_time = 0
            return self.input

    def roll(self):
        return self.held_key  # todo, slow to once per couple frames



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
