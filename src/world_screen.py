import screen
import world_drawing
import world_screen_content
import user_input
import pygame


class MainGameScreen(screen.GameScreen):
    def __init__(self, display, session):
        screen.GameScreen.__init__(self, display, session)
        self.content = world_screen_content.MapAndUI()
        self.animation = world_drawing.MapDrawing(self.content, display)

    def execute_tick(self):
        #  Game logic goes here
        self.animation.execute_tick()

    def receive_input(self, curr_input: user_input.Input):
        pass
