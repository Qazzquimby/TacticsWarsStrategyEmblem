import commands
import directions
import points
import user_input
import world_screen


class MoveCursor(commands.Command):
    direction = NotImplemented

    def __init__(self, target: "Cursor", content: "world_screen.MapAndUI"):
        commands.Command.__init__(self, target, content)

    def move_to(self, point: points.MapPoint):
        self.target.location = point
        self.content.map_drawing.scroll_to_cursor()

    def center(self):
        """Center the cursor on the map."""
        self.move_to(points.MapPoint(int(self.content.map.width / 2), int(self.content.map.height / 2)))

    def execute(self):
        new_tile = self.target.location.directed_neighbour(self.direction)
        if self.content.map.has_point(new_tile):
            self.move_to(new_tile)


class MoveCursorRight(MoveCursor):
    direction = directions.Right

    def __init__(self, target: "Cursor", content: "world_screen.MapAndUI"):
        MoveCursor.__init__(self, target, content)


class MoveCursorLeft(MoveCursor):
    direction = directions.Left

    def __init__(self, target: "Cursor", content: "world_screen.MapAndUI"):
        MoveCursor.__init__(self, target, content)


class MoveCursorUp(MoveCursor):
    direction = directions.Up

    def __init__(self, target: "Cursor", content: "world_screen.MapAndUI"):
        MoveCursor.__init__(self, target, content)


class MoveCursorDown(MoveCursor):
    direction = directions.Down

    def __init__(self, target: "Cursor", content: "world_screen.MapAndUI"):
        MoveCursor.__init__(self, target, content)


class Cursor(object):
    def __init__(self, world_map: "world_screen.Map"):
        self.map = world_map
        self.location = points.MapPoint(0, 0)
        # self.center()

    def receive_input(self, curr_input: user_input.Input):
        if curr_input == user_input.Right:
            return MoveCursorRight
        elif curr_input == user_input.Left:
            return MoveCursorLeft
        elif curr_input == user_input.Up:
            return MoveCursorUp
        elif curr_input == user_input.Down:
            return MoveCursorDown
