import typing

import pygame

import commands
import cursor
import directions
import entities
import graphics
import layers
import points
import screens
import sprites
import user_input
from world_setups import WorldSetup


class MainGameScreen(screens.GameScreen):
    """Screen, interface for world content"""

    def __init__(self, screen_engine, world_setup):
        screens.GameScreen.__init__(self, screen_engine)
        self.world_setup = world_setup
        self.content = MapAndUI(self.world_setup, self.display)
        self.name = "Main Game Screen"

    def execute_tick(self):
        #  Game logic goes here
        self.content.map_drawing.execute_tick()

    def _receive_input(self, curr_input: user_input.Input):
        self.content.receive_input(curr_input)


class MapAndUI(object):
    """Packages game screen elements"""

    def __init__(self, world_setup, display):
        self.top_bar = TopBar()
        self.map = Map(world_setup)
        self.world_menu = WorldMenu()
        self.map_drawing = MapDrawing(self, display)

        self.selection = None  # Entity currently being manipulated

    def receive_input(self, curr_input: user_input.Input):
        selection = self.selection
        if selection is None:
            selection = self.map.cursor

        command = selection.receive_input(curr_input)  # type: typing.Optional[typing.Type[commands.Command]]
        if command is not None:
            command(selection, self).execute()


class Tile(object):
    """A square on the map"""

    def __init__(self,
                 tile_terrain: "entities.Terrain",
                 building: typing.Union["entities.Building", "entities.NullEntity"],
                 unit: typing.Union["entities.Unit", "entities.NullEntity"]):
        self.terrain = tile_terrain
        self.building = building
        self.unit = unit


class Map(object):
    def __init__(self, world_setup: "WorldSetup"):
        self.world_setup = world_setup  # type: WorldSetup
        self._map = self._init_map(
            self.world_setup.map_setup.entity_seed_array)  # type: typing.List[typing.List[Tile]]

        self.size_point = points.ScreenPoint.from_tile(self.width, self.height)
        self.surface = graphics.make_surface(self.size_point.pixel)

        self.cursor = cursor.Cursor(self)  # type: cursor.Cursor

    def has_point(self, point: points.MapPoint):
        if point.tile_x >= 0 and point.tile_y >= 0:
            if point.tile_x < self.size_point.tile_x and point.tile_y < self.size_point.tile_y:
                return True
        return False

    def get_entities(self, layer: typing.Type["layers.Layer"], map_point: points.MapPoint) -> "entities.Entity":
        if layer == layers.TerrainLayer:
            return self.get_terrain(map_point)
        elif layer == layers.BuildingLayer:
            return self.get_building(map_point)
        elif layer == layers.UnitLayer:
            return self.get_unit(map_point)
        else:
            raise TypeError

    def get_terrain(self, map_point: points.MapPoint) -> "entities.Terrain":
        tile = self.get_tile(map_point)
        terrain = tile.terrain
        return terrain

    def get_building(self, map_point: points.MapPoint) -> "entities.Building":
        tile = self.get_tile(map_point)
        building = tile.building
        return building

    def get_unit(self, map_point: points.MapPoint) -> "entities.Unit":
        tile = self.get_tile(map_point)
        unit = tile.unit
        return unit

    def get_tile(self, map_point: points.MapPoint) -> Tile:
        return self._map[map_point.tile_x][map_point.tile_y]

    @property
    def width(self) -> int:
        return len(self._map)

    @property
    def height(self) -> int:
        return len(self._map[0])

    def _init_map(self, entity_seed_array: list):
        world_map = []
        for column in entity_seed_array:
            column = self._create_column(column)
            world_map.append(column)
        return world_map

    def _create_column(self, column: list):
        tiles = []
        for seed_tile in column:
            tile_terrain = self.world_setup.entity_from_seed(seed_tile.terrain)
            tile_building = self.world_setup.entity_from_seed(seed_tile.building)
            tile_unit = self.world_setup.entity_from_seed(seed_tile.unit)

            tile = Tile(tile_terrain, tile_building, tile_unit)
            tiles.append(tile)
        return tiles


class TopBar(object):
    def __init__(self):
        self.surface = sprites.SpriteAnimation("", "sprites/top_bar").sprite_sheet.original_sprite_sheet_surface


class WorldMenu(object):
    def __init__(self):
        self.surface = sprites.SpriteAnimation("", "sprites/world_menu").sprite_sheet.original_sprite_sheet_surface


class ViewPort(object):
    def __init__(self, world_map: Map):
        self.map = world_map  # type: Map

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

        self.SCROLL_BOUNDARY = 2

    @property
    def range_x(self):
        return range(self.map_start_point.tile_x,
                     self.map_start_point.tile_x + self.size_point.tile_x)

    @property
    def range_y(self):
        return range(self.map_start_point.tile_y,
                     self.map_start_point.tile_y + self.size_point.tile_y)

    @property
    def map_end_point(self):
        return self.map_start_point + self.size_point

    def scroll_one_tile(self, direction: directions.Direction):
        if direction in self.get_scrollable_edges():
            self.map_start_point = self.map_start_point + direction.point

    def get_scrollable_edges(self):
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

    def _init_size_point(self) -> points.ScreenPoint:
        size_tile_x = min(self.map.size_point.tile_x, graphics.SCREEN_TILE_WIDTH)
        size_tile_y = min(self.map.size_point.tile_y, graphics.MENU_TILE_HEIGHT)

        self.size_point = points.ScreenPoint.from_tile(size_tile_x, size_tile_y)

    def _init_draw_point(self) -> points.ScreenPoint:
        map_padding_x = graphics.MAP_TILE_WIDTH - self.map.width
        half_padding_x = int(map_padding_x / 2)
        screen_draw_tile_x = max(half_padding_x, 0)

        map_padding_y = graphics.MAP_TILE_HEIGHT - self.map.height
        half_padding_y = int(map_padding_y / 2)
        translated_half_padding_y = half_padding_y + graphics.TOP_BAR_TILE_HEIGHT
        screen_draw_tile_y = max(translated_half_padding_y, 0)

        self.draw_point = points.ScreenPoint.from_tile(screen_draw_tile_x,
                                                       screen_draw_tile_y)

    def _init_end_point(self) -> points.ScreenPoint:
        self.end_point = self.draw_point + self.size_point


class MapDrawing(object):
    def __init__(self, content: MapAndUI, display: graphics.Display):
        self.display = display  # type: graphics.Display
        self.content = content
        self.top_bar = self.content.top_bar
        self.map = content.map  # type: Map
        self.viewport = ViewPort(self.map)
        self.world_menu = content.world_menu

        self.map_larger_than_screen = self._init_map_larger_than_screen()

    def execute_tick(self):
        self.draw_map()
        self.draw_top_bar()
        self.draw_world_menu()

    def draw_top_bar(self):
        sprite = self.top_bar.surface
        map_point = points.MapPoint(0, 0)
        self.display.blit(sprite, map_point.pixel)

    def draw_map(self):
        for layer in [layers.TerrainLayer, layers.BuildingLayer, layers.UnitLayer]:
            self.draw_map_layer(layer)
        self.draw_cursor()
        self.draw_map_surface()

    def draw_map_layer(self, layer: typing.Type[layers.Layer]):
        for screen_x, map_x in enumerate(self.viewport.range_x):
            for screen_y, map_y in enumerate(self.viewport.range_y):
                map_point = points.MapPoint.from_tile(map_x, map_y)
                screen_point = points.ScreenPoint.from_tile(screen_x, screen_y)
                self.draw_tile_layer(layer, map_point, screen_point)

    def draw_tile_layer(self, layer: typing.Type[layers.Layer], map_point: points.MapPoint,
                        screen_point: points.ScreenPoint):
        entity = self.map.get_entities(layer, map_point)
        self.draw_entity_if_not_null_entity(entity, screen_point)

    def draw_entity_if_not_null_entity(self, entity: "entities.Entity",
                                       screen_point: points.ScreenPoint):
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
        self.map.surface.blit(self.map.cursor.sprite, (self.map.cursor.location - self.viewport.map_start_point).pixel)

    def draw_map_surface(self):
        self.display.blit(self.map.surface, self.viewport.draw_point.pixel)

    def draw_world_menu(self):
        sprite = self.world_menu.surface
        menu_top_tile = graphics.TOP_BAR_TILE_HEIGHT + graphics.MAP_TILE_HEIGHT
        screen_point = points.ScreenPoint.from_tile(0, menu_top_tile)
        self.display.blit(sprite, screen_point.pixel)

    def _init_map_larger_than_screen(self) -> bool:
        is_taller = self.map.height > graphics.MAP_TILE_HEIGHT
        is_wider = self.map.width > graphics.MAP_TILE_WIDTH
        is_larger = is_taller or is_wider
        return is_larger

    def _init_map_position(self) -> points.ScreenPoint:
        if self.map_larger_than_screen:
            return points.ScreenPoint(0, 0 + graphics.TOP_BAR_HEIGHT)
        else:
            centered_x = int((graphics.MAP_TILE_WIDTH - self.map.width) / 2)
            centered_y = int((graphics.MAP_TILE_HEIGHT - self.map.height) / 2 +
                             graphics.TOP_BAR_TILE_HEIGHT)
            return points.ScreenPoint.from_tile(centered_x, centered_y)

    def scroll_to_cursor(self):
        scrollable_edges = self.viewport.get_scrollable_edges()
        for direction in scrollable_edges:
            if self.is_cursor_in_scroll_area(direction):
                self._scroll_to_cursor_in_boundary(direction)

    def is_cursor_in_scroll_area(self, direction: directions.Direction):
        if direction is directions.RIGHT:
            return self.map.cursor.location.tile_x >= self.viewport.map_end_point.tile_x - self.viewport.SCROLL_BOUNDARY
        elif direction is directions.LEFT:
            return self.map.cursor.location.tile_x <= self.viewport.map_start_point.tile_x + self.viewport.SCROLL_BOUNDARY
        elif direction is directions.UP:
            return self.map.cursor.location.tile_x <= self.viewport.map_start_point.tile_x + self.viewport.SCROLL_BOUNDARY
        elif direction is directions.DOWN:
            return self.map.cursor.location.tile_y >= self.viewport.map_end_point.tile_y - self.viewport.SCROLL_BOUNDARY
        else:
            raise ValueError("Bad direction given")

    def is_cursor_out_of_viewport(self):
        cursor_point = self.map.cursor.location
        return cursor_point.tile_x in self.viewport.range_x \
               and cursor_point.tile_y in self.viewport.range_y

    def _scroll_to_cursor_in_boundary(self, direction: directions.Direction):
        """If the cursor is off the boundary in the given direction, scroll until it is within the boundary."""
        while self.is_cursor_in_scroll_area(direction):
            self.viewport.scroll_one_tile(direction)
