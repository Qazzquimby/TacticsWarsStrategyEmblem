from unittest import TestCase

import graphics
import screens
import session


class TestScreenEngine(TestCase):
    def setUp(self):
        self.display = graphics.Display()
        self.session = session.Session()
        self.state_engine = screens.ScreenEngine(self.display, self.session)

    def test_len_after_one_push(self):
        self.state_engine.push_screen(screens.EmptyScreen())
        assert (len(self.state_engine._screen_stack) == 1)

    def test_pop_on_empty_stack_ends_game(self):
        self.state_engine.pop_screen()
        assert (self.session._game_running is False)

    def test_len_after_push_push_pop(self):
        self.state_engine.push_screen(screens.EmptyScreen())
        self.state_engine.push_screen(screens.EmptyScreen())
        self.state_engine.pop_screen()
        assert (len(self.state_engine._screen_stack) == 1)

    def test_switch_screen(self):
        print("a")
        self.setUp()
        print("b")
        first_screen = screens.EmptyScreen()
        second_screen = screens.EmptyScreen()

        self.state_engine.push_screen(first_screen)
        self.state_engine.switch_screen(second_screen)
        assert (self.state_engine.screen is second_screen)
        assert (len(self.state_engine._screen_stack) == 1)
