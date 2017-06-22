import screen
import map_drawing


class MainGameScreen(screen.GameScreen):
    def __init__(self, display, session):
        screen.GameScreen.__init__(self, display, session)
        self.content = map_drawing.MapDrawing()

