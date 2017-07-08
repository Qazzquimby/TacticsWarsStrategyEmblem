import screen
import map_drawing
import game_map_and_menu
import user_input


class MainGameScreen(screen.GameScreen):
    def __init__(self, display, session):
        screen.GameScreen.__init__(self, display, session)
        self.content = game_map_and_menu.MapAndUI()
        self.animation = map_drawing.MapDrawing(self.content, display)

    def execute_tick(self):
        #  Game logic goes here
        self.animation.execute_tick()

    def receive_input(self, curr_input: user_input.Input):
        pass
