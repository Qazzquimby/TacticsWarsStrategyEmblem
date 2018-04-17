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

"""Top level structures for the main game screen."""

import pygame

import cursor
import directions
import graphics
import layers
import points
import screens
import sprites


class MainGameScreen(screens.GameScreen):
    """Screen, interface for world content

    Attributes:
        self.world_setup (WorldSetup): A blueprint object to build the world with.
        self.content (MapAndUI): Holds implementation of all world content.
        self.name (str): Friendly name of the screen.
    """

    def __init__(self, screen_engine, world_setup):
        screens.GameScreen.__init__(self, screen_engine)
        self.world_setup = world_setup
        self.content = MapAndUI(self.world_setup, self.display)
        self.name = "Main Game Screen"

    def execute_tick(self):
        """Runs a single tick of game logic, and updates the display's surface."""
        #  TODO Game logic goes here
        self.content.map_drawing.execute_tick()

    def _receive_input(self, curr_input):
        """Passes user input to content.

        Args:
            curr_input (user_input.Input): The input to be passed.
        """
        self.content.receive_input(curr_input)


class MapAndUI(object):
    """Packages game screen elements

    Attributes:
        self.top_bar (TopBar): The hud display at the top of the screen.
        self.map (Map): The map on which the game is played.
        self.world_menu (WorldMenu): The menu displayed during the game at the bottom of the screen.
        self.map_drawing (MapDrawing): The class handling displaying the contents of the map.
        self._selection (Optional[Entity]): The entity currently being manipulated.
    """

    def __init__(self, world_setup, display):
        self.top_bar = TopBar()
        self.map = Map(world_setup)
        self.world_menu = WorldMenu()
        self.map_drawing = MapDrawing(self, display)

        self.selection = None

    def receive_input(self, curr_input):
        """Takes user input and interacts with the world based on context.

        If something is selected, the input is sent to the _selection.
        If nothing is selected, moves the cursor.

        Receives a command in response, executes the command.

        Args:
            curr_input (user_input.Input): The input to route.
        """
        selection = self.selection
        if selection is None:
            selection = self.map.cursor

        command = selection.receive_input(curr_input)
        if command is not None:
            command(selection, self).execute()


class Tile(object):
    """A square of fixed size on the map.
    Tiles contain 3 layers: terrain, building, and unit, which can each contain an entity.

    Attributes:
        self.terrain (entities.Terrain): The tile's terrain entity.
        self.building (Optional[entites.Building]): The tile's building entity.
        self.unit (Optional[entites.Unit]): The tile's unit entity.
    """

    def __init__(self, tile_terrain, building, unit):
        self.terrain = tile_terrain
        self.building = building
        self.unit = unit


class Map(object):
    """Contains the grid which holds all entities, and related functionality.

    Attributes:
        self.world_setup (WorldSetup): The blueprint object that is used to initialize the world.
        self.size_point (points.ScreenPoint): The point at the bottom right corner of the full map.
        self.surface (pygame.Surface): A Surface onto which the map is drawn before it is stamped
            onto the main display surface.
        self.cursor (cursor.Cursor): the cursor object which the player uses to select things.
    """

    def __init__(self, world_setup):
        self.world_setup = world_setup
        self._map = self._init_map(self.world_setup.map_setup.entity_seed_grid)

        self.size_point = points.ScreenPoint.from_tile(self.width, self.height)
        self.surface = graphics.make_surface(self.size_point.pixel)

        self.cursor = cursor.Cursor(self)

    def has_point(self, point: points.MapPoint):
        """Returns whether or not a point is on the map.

        Args:
            point (points.MapPoint): The point to check.

        Returns:
            boolean: If the point is within the boundaries of the map.
        """
        if point.tile_x >= 0 and point.tile_y >= 0:
            if point.tile_x < self.size_point.tile_x and point.tile_y < self.size_point.tile_y:
                return True
        return False

    def get_entity_from_map(self, layer, map_point):
        """Gets the entity from a given layer and map point.

        Args:
            layer (layers.Layer): The entity's layer.
            map_point (points.MapPoint): The entity's coordinates on the map.

        Returns:
            entities.Entity: The entity found.
        """
        if layer == layers.TerrainLayer:
            return self.get_terrain(map_point)
        elif layer == layers.BuildingLayer:
            return self.get_building(map_point)
        elif layer == layers.UnitLayer:
            return self.get_unit(map_point)
        else:
            raise TypeError

    def get_terrain(self, map_point):
        """Gets the terrain entity from a given map point.
        Args:
            map_point (points.MapPoint): The terrain's coordinates
        Returns:
            entities.Terrain: The terrain found.
        """
        tile = self.get_tile(map_point)
        terrain = tile.terrain
        return terrain

    def get_building(self, map_point):
        """Gets the building entity from a given map point, or a Null Entity if none is found.
        Args:
            map_point (points.MapPoint): The building's coordinates
        Returns:
            entities.Building or entities.NullEntity: The building found.
        """
        tile = self.get_tile(map_point)
        building = tile.building
        return building

    def get_unit(self, map_point):
        """Gets the unit entity from a given map point, or a Null Entity if none is found.
        Args:
            map_point (points.MapPoint): The unit's coordinates
        Returns:
            entities.Unit or entities.NullEntity: The unit found.
        """
        tile = self.get_tile(map_point)
        unit = tile.unit
        return unit

    def get_tile(self, map_point):
        """Returns the tile at the given coordinates.

        Args:
            map_point (points.MapPoint): The coordinates to take the tile from.

        Returns:
            Tile: The tile at the coordinates.
        """
        return self._map[map_point.tile_x][map_point.tile_y]

    @property
    def width(self):
        """int: The width of the map in tiles."""
        return len(self._map)

    @property
    def height(self):
        """int: The height of the map in tiles."""
        return len(self._map[0])

    def _init_map(self, entity_seed_grid: list):
        """Initialize the map from the given entity_seed_grid.

        Args:
            entity_seed_grid (list): A list of columns of entity seeds

        Returns:
            The generated map of instantiated entities.
        """
        world_map = []
        for column in entity_seed_grid:
            column = self._create_column(column)
            world_map.append(column)
        return world_map

    def _create_column(self, column: list):
        """Initialize a column map from the given column of an entity_seed_grid.

        Args:
            column (list): A list of entity seeds

        Returns:
            A column of instantiated entities.
        """
        tiles = []
        for seed_tile in column:
            tile_terrain = self.world_setup.entity_from_seed(seed_tile.terrain)
            tile_building = self.world_setup.entity_from_seed(seed_tile.building)
            tile_unit = self.world_setup.entity_from_seed(seed_tile.unit)

            tile = Tile(tile_terrain, tile_building, tile_unit)
            tiles.append(tile)
        return tiles


class TopBar(object):
    """The hud display at the top of the screen."""

    def __init__(self):
        sprite_sheet = sprites.SpriteAnimation("", "assets/top_bar").sprite_sheet
        self.surface = sprite_sheet.original_sprite_sheet_surface


class WorldMenu(object):
    """The in-game menu at the bottom of the screen."""

    def __init__(self):
        sprite_sheet = sprites.SpriteAnimation("", "assets/world_menu").sprite_sheet
        self.surface = sprite_sheet.original_sprite_sheet_surface


class ViewPort(object):
    """The window between the top bar and the map menu where the map is displayed.
    The map may be smaller or larger than this area.

    This does not modify the map.

    Attributes:
        self.map (Map): The map being displayed.
        self.size_point (points.ScreenPoint): The bottom right corner of the map, starting at (0,0).
        self.draw_point (points.ScreenPoint): The top left corner of the map, where it should be
            drawn.
        self.map_start_point(points.MapPoint): The tile on the map which is drawn at the top left
            corner. Due to scrolling, it may not be the top left corner of the actual map.
        self.scroll_boundary (int): The number of tiles around the edge of the map which will
            cause the map to scroll if entered by the cursor.
    """

    def __init__(self, world_map: Map):
        self.map = world_map

        # size of the viewport
        self.size_point = NotImplemented  # type: points.ScreenPoint
        self._init_size_point()

        # top left corner of viewport drawing
        self.draw_point = NotImplemented  # type: points.ScreenPoint
        self._init_draw_point()

        # bottom right corner of viewport drawing
        self.end_point = NotImplemented  # type: points.ScreenPoint
        self._init_end_point()

        self.map_start_point = points.MapPoint.from_tile(0, 0)  # type: points.MapPoint

        self.scroll_boundary = 2

    @property
    def range_x(self):
        """list(int): The range of tile x map oordinates that are visible in the viewport."""
        return range(self.map_start_point.tile_x,
                     self.map_start_point.tile_x + self.size_point.tile_x)

    @property
    def range_y(self):
        """list(int): The range of tiles y map coordinates that are visible in the viewport."""
        return range(self.map_start_point.tile_y,
                     self.map_start_point.tile_y + self.size_point.tile_y)

    @property
    def map_end_point(self):
        """points.MapPoint: The bottom right point of the map which is drawn to the viewport."""
        return self.map_start_point + self.size_point

    def scroll_one_tile(self, direction: directions.Direction):
        """Moves the map within the viewport, changing which tiles are visisble, based on the
        given direction.

        Args:
            direction directions.Direction: The direction to scroll in.
        """
        if direction in self.get_scrollable_edges():
            self.map_start_point = self.map_start_point + direction.point

    def get_scrollable_edges(self):
        """Returns a list of directions in which the map can scroll.

        Returns:
            list[directions.Direction]: The list of directions.
        """
        scrollable_edges = []
        if self.map_start_point.tile_x > 0:
            scrollable_edges.append(directions.LEFT)
        if self.map_start_point.tile_y > 0:
            scrollable_edges.append(directions.UP)
        if self.map_start_point.tile_x + self.size_point.tile_x < self.map.size_point.tile_x:
            scrollable_edges.append(directions.RIGHT)
        if self.map_start_point.tile_y + self.size_point.tile_y < self.map.size_point.tile_y:
            scrollable_edges.append(directions.DOWN)
        return scrollable_edges

    def _init_size_point(self):
        """Initializes the size point.
        The size point is the minimum of the size of the map and the size of the viewport.
        """
        size_tile_x = min(self.map.size_point.tile_x, graphics.SCREEN_TILE_WIDTH)
        size_tile_y = min(self.map.size_point.tile_y, graphics.MENU_TILE_HEIGHT)

        self.size_point = points.ScreenPoint.from_tile(size_tile_x, size_tile_y)

    def _init_draw_point(self):
        """Initializees the draw point.
        The draw point is under the top bar, and visually centered if the map is smaller than the
        viewport.
        """
        map_padding_x = graphics.MAP_TILE_WIDTH - self.map.width
        half_padding_x = int(map_padding_x / 2)
        screen_draw_tile_x = max(half_padding_x, 0)

        map_padding_y = graphics.MAP_TILE_HEIGHT - self.map.height
        half_padding_y = int(map_padding_y / 2)
        translated_half_padding_y = half_padding_y + graphics.TOP_BAR_TILE_HEIGHT
        screen_draw_tile_y = max(translated_half_padding_y, 0)

        self.draw_point = points.ScreenPoint.from_tile(screen_draw_tile_x,
                                                       screen_draw_tile_y)

    def _init_end_point(self):
        self.end_point = self.draw_point + self.size_point


class MapDrawing(object):
    """Handles drawing the contents of the map screen.

    Draws the hud and map onto the display surface

    Attributes:
        self.display (graphics.Display): The display to draw to.
        self.content (MapAndUI): The screen elements
        self.top_bar (TopBar): The top hud element.
        self.map (Map): The map.
        self.viewport (ViewPort): The visible area of the map on screen.
        self.world_menu (WorldMenu): The in game menu at the bottom of the screen.
    """

    def __init__(self, content: MapAndUI, display: graphics.Display):
        self.display = display
        self.content = content
        self.top_bar = self.content.top_bar
        self.map = content.map
        self.viewport = ViewPort(self.map)
        self.world_menu = content.world_menu

        self.map_larger_than_screen = self._init_map_larger_than_screen()

    def execute_tick(self):
        """Called every tick. Draws the map and hud elements."""
        self.draw_map()
        self.draw_top_bar()
        self.draw_world_menu()

    def draw_top_bar(self):
        """Draws the top bar."""
        sprite = self.top_bar.surface
        map_point = points.MapPoint(0, 0)
        self.display.blit(sprite, map_point.pixel)

    def draw_map(self):
        """Draws the map, layer by layer, followed by the cursor."""
        for layer in [layers.TerrainLayer, layers.BuildingLayer, layers.UnitLayer]:
            self.draw_map_layer(layer)
        self.draw_cursor()
        self.draw_map_surface()

    def draw_map_layer(self, layer):
        """Draws a given layer of the map.
        Args:
            layer (typing.Type[layers.Layer]:
        """
        for screen_x, map_x in enumerate(self.viewport.range_x):
            for screen_y, map_y in enumerate(self.viewport.range_y):
                map_point = points.MapPoint.from_tile(map_x, map_y)
                screen_point = points.ScreenPoint.from_tile(screen_x, screen_y)
                self.draw_tile_layer(layer, map_point, screen_point)

    def draw_tile_layer(self, layer, map_point, screen_point):
        """Draws a given layer of a given tile.
        Args:
            layer (typing.Type[layers.Layer]): The layer to draw.
            map_point (points.MapPoint): The coordinates of the space to draw.w
            screen_point (points.ScreenPoint): The point on the screen to draw the tile.
        """
        entity = self.map.get_entity_from_map(layer, map_point)
        self.draw_entity_if_not_null_entity(entity, screen_point)

    def draw_entity_if_not_null_entity(self, entity, screen_point):
        """Draws a given entity, if it exists.

        Args:
            entity (entities.Entity): The entity to draw.
            screen_point (points.ScreenPoint): The point on the screen to draw the entity.
        """
        try:
            self._draw_entity_if_sprite_found(entity, screen_point)
        except sprites.DrawNullEntityException:
            pass

    def _draw_entity_if_sprite_found(self, entity: "entities.Entity",
                                     screen_point: points.ScreenPoint):
        sprite = entity.sprite
        if sprite:
            self._draw_entity_sprite(sprite, screen_point)
        else:
            raise sprites.MissingSpriteException

    def _draw_entity_sprite(self, sprite: pygame.Surface, screen_point: points.ScreenPoint):
        self.map.surface.blit(sprite, screen_point.pixel)

    def draw_cursor(self):
        """Draws the cursor at its correct location on the screen."""
        self.map.surface.blit(self.map.cursor.sprite,
                              (self.map.cursor.location - self.viewport.map_start_point).pixel)

    def draw_map_surface(self):
        """Draws the blueprint surface onto the main display surface."""
        self.display.blit(self.map.surface, self.viewport.draw_point.pixel)

    def draw_world_menu(self):
        """Draws the in game menu at the bottom of the screen."""
        sprite = self.world_menu.surface
        menu_top_tile = graphics.TOP_BAR_TILE_HEIGHT + graphics.MAP_TILE_HEIGHT
        screen_point = points.ScreenPoint.from_tile(0, menu_top_tile)
        self.display.blit(sprite, screen_point.pixel)

    def _init_map_larger_than_screen(self) -> bool:
        """Gets if the map is larger than the viewport window in any dimension.
            Returns:
                boolean: If the map is larger.
        """
        is_taller = self.map.height > graphics.MAP_TILE_HEIGHT
        is_wider = self.map.width > graphics.MAP_TILE_WIDTH
        is_larger = is_taller or is_wider
        return is_larger

    def _init_map_position(self):
        """Gets the top left point to draw the map in the viewport.
        Is (0,0) of the viewport if the map is the same size or larger.
        Else it centers the map in the viewport as much as possible.

        Returns:
            points.ScreenPoint: The point to draw the map to.
        """
        if self.map_larger_than_screen:
            return points.ScreenPoint(0, 0 + graphics.TOP_BAR_HEIGHT)
        else:
            centered_x = int((graphics.MAP_TILE_WIDTH - self.map.width) / 2)
            centered_y = int((graphics.MAP_TILE_HEIGHT - self.map.height) / 2 +
                             graphics.TOP_BAR_TILE_HEIGHT)
            return points.ScreenPoint.from_tile(centered_x, centered_y)

    def scroll_to_cursor(self):
        """Scrolls the map towards the cursor until the cursor is inside the scroll boundary."""
        scrollable_edges = self.viewport.get_scrollable_edges()
        for direction in scrollable_edges:
            if self._is_cursor_in_scroll_area(direction):
                self._scroll_to_cursor_in_boundary(direction)

    def _scroll_to_cursor_in_boundary(self, direction: directions.Direction):
        """If the cursor is off the boundary in the given direction, scroll until it is within
        the boundary."""
        while self._is_cursor_in_scroll_area(direction):
            self.viewport.scroll_one_tile(direction)

    def _is_cursor_in_scroll_area(self, direction: directions.Direction):
        """Gets if the cursor is outside the scroll boundary in the given direction.

        The scroll boundary usually has a buffer around the edge of the viewport, so that the
        screen will scroll before the cursor reaches the edge, unless there is no more map to
        scroll.

        Args:
            direction (directions.Direction): The direction to check

        Returns:
            boolean: If the cursor is outside the scroll boundary.
        """
        if direction is directions.RIGHT:
            boundary = self.viewport.map_end_point.tile_x - self.viewport.scroll_boundary
            return self.map.cursor.location.tile_x >= boundary

        elif direction is directions.LEFT:
            boundary = self.viewport.map_start_point.tile_x + self.viewport.scroll_boundary
            return self.map.cursor.location.tile_x <= boundary

        elif direction is directions.UP:
            boundary = self.viewport.map_start_point.tile_x + self.viewport.scroll_boundary
            return self.map.cursor.location.tile_x <= boundary

        elif direction is directions.DOWN:
            boundary = self.viewport.map_end_point.tile_y - self.viewport.scroll_boundary
            return self.map.cursor.location.tile_y >= boundary
        else:
            raise ValueError("Bad direction given")
