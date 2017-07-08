import screen
import map_drawing
import game_map_and_menu
import user_input


class MainGameScreen(screen.GameScreen):
    def __init__(self, display, session):
        screen.GameScreen.__init__(self, display, session)
        self.content = game_map_and_menu.GameMap()
        self.animation = map_drawing.MapDrawing(self.content, display)

    def execute_tick(self):
        # TODO  Game logic here
        self.animation.execute_tick()

    def receive_input(self, curr_input: user_input.Input):
        pass