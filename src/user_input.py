# MIT License
# Copyright (c) 2018 Toren James Darby
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Classes related to receiving and interpreting user input

Attributes:
    KEY_UP (int):  A simple enumeration for lifting a key.
    KEY_DOWN (int):  A simple enumeration for pressing a key.

    QUIT (Input): An input to immediately quit the game. Temporary.
    CONFIRM (Input): An input to confirm or make a _selection.
    BACK (Input): An input to back out of the current _selection.
    LEFT (Input): An input to move left.
    UP (Input): An input to move up.
    RIGHT (Input): An input to move right.
    DOWN (Input): An input to move down.

    STOP_LEFT (Input): An input to stop moving left.
    STOP_UP (Input): An input to stop moving up.
    STOP_RIGHT (Input): An input to stop moving right.
    STOP_DOWN (Input): An input to stop moving down.

    HELD_INPUTS (List[Input]): A list of inputs which can be held.
    HELD_INPUT_LIFTS (List[Input]): A list of inputs which terminate held inputs.
"""

import typing
from collections import OrderedDict

import pygame

KEY_UP = 1
KEY_DOWN = 2


class Input(object):
    """An input that the game can understand. Not all keys are necessarily mapped to inputs.

    Attributes:
        self.name (str): The name of the input, for debugging.
        self.priority (int): Used for comparing inputs. Lower priorities overwrite higher
        priorities in the same frame.
    """

    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

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
    """Handles converting all key changes to a single action
    Attributes:
          self.control_map (ControlMap): Routes key presses to Inputs.
          self.held_keys (list[Input]): All keys currently held.
          self.input_repeater (InputRepeater): Handles input from held keys.
    """

    def __init__(self):
        self.control_map = ControlMap()
        self.held_keys = []
        self.input_repeater = InputRepeater(self)

    @property
    def held_key(self):
        """Input: The most recent key to be held."""
        try:
            return self.held_keys[-1]
        except IndexError:
            return None

    def interpret_input(self) -> typing.Optional[Input]:
        """Returns the action to be performed this frame.

        Looks at this frame's key presses, maps them to their inputs,
        then returns the one with the lowest priority."""

        inputs, lifts = self._get_inputs()

        self.process_lifts(lifts)
        curr_input = self.process_inputs(inputs)
        self.process_lifts(lifts)
        return curr_input

    def _get_inputs(self):
        """Maps this frame's key presses and lifts to their Inputs

        For each keypress, determine if it maps to an input or lift, and return lists of all
        inputs and lifts found.

        Returns:
            inputs (list[Input]): All mapped inputs found.
            lifts (list[Input]): All mapped lifts found.
        """
        inputs = []
        lifts = []
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
                curr_input = self.control_map.key_to_input((pygame.key.name(event.key), KEY_DOWN))
                if curr_input:
                    inputs.append(curr_input)

            elif event.type == pygame.KEYUP:  # pylint: disable=no-member
                curr_input = self.control_map.key_to_input((pygame.key.name(event.key), KEY_UP))
                if curr_input:
                    lifts.append(curr_input)

        return inputs, lifts

    def process_lifts(self, lifts):
        """For each lift, terminate their corresponding held key if it is active.

        Args:
            lifts (typing.List[Lift]): All lifts to process.
        """
        for lift in lifts:
            assert lift in HELD_INPUT_LIFTS
            print("lift", lift.name)
            push_action = self.lift_action_to_push_action(lift)
            if push_action in self.held_keys:
                print("LIFTED")
                self.held_keys.remove(push_action)

    @staticmethod
    def lift_action_to_push_action(lift):
        """Get the corresponding keypress from a lift.

        Args:
            lift (Input): The lift to map.

        Returns:
            Input: The resulting keypress.
        """
        lifted = HELD_INPUTS[HELD_INPUT_LIFTS.index(lift)]
        return lifted

    def process_inputs(self, inputs):
        """Overwrites held keys with new key presses, or sustains the key.

        Args:
            inputs (typing.List[Input]): The inputs to process.

        Returns:
            The single input to use this frame.
        """
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

    def _held_key_input(self):
        # todo improve cursor movement
        return self.input_repeater.input


class InputRepeater(object):
    """Handles repeating input from held keys.

    Attributes:
        self.input_interpreter (InputInterpreter): Gives access to input interpretation functions.
        self.current_hold_time (int): The number of frames the key has currently been held.
        self.hold_time_before_roll (int): The number of frames a key must be held before it will
        repeat its action.
        self.hold_time_per_roll (int): The number of frames a key must be held before it will
        repeat its action after it has already repeated at least once.
        self.held_key (Input): The key which is being held.
    """

    def __init__(self, input_interpreter):
        self.input_interpreter = input_interpreter
        self.current_hold_time = 0
        self.hold_time_before_roll = 8
        self.hold_time_per_roll = 2
        self.held_key = None

    @property
    def input(self):
        """Input: The currently held key."""
        if self.input_interpreter.held_key == self.held_key:
            return self._repeat_input()
        else:
            return self._change_key()

    def _repeat_input(self):
        if self.current_hold_time < self.hold_time_before_roll:
            curr_input = None
        else:
            curr_input = self._roll()
        self.current_hold_time += 1
        return curr_input

    def _change_key(self):
        self.held_key = self.input_interpreter.held_key
        self.current_hold_time = 0
        return self.input

    def _roll(self):
        if self.current_hold_time % self.hold_time_per_roll == 0:
            return self.held_key
        else:
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
