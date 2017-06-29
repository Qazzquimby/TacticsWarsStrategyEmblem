import screen
import map_drawing
import game_map_and_menu


class MainGameScreen(screen.GameScreen):
    def __init__(self, display, session):
        screen.GameScreen.__init__(self, display, session)
        self.content = game_map_and_menu.GameMap()
        self.animation = map_drawing.MapDrawing(self.content)
