from unittest import TestCase

import graphics
import screens
import sessionmod


class TestScreenEngine(TestCase):
    def setUp(self):
        self.display = graphics.Display()
        self.session = sessionmod.Session()
        self.state_engine = screens.ScreenEngine(self.display, self.session)

    def test_setup_initial_screen(self):
        self.state_engine.setup_initial_screen()
        if len(self.state_engine._screen_stack) > 0:
            self.fail()

    def test_something_else(self):
        self.fail()


class TestTest(TestCase):
    def test___init__(self):
        self.fail()
