import typing

import pygame

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
        self.content = MapAndUI(self.world_setup)
        self.animation = MapDrawing(self.content, self.display)
        self.name = "Main Game Screen"

    def execute_tick(self):
        #  Game logic goes here
        self.animation.execute_tick()

    def _receive_input(self, curr_input: user_input.Input):
        self.content.receive_input(curr_input)


class MapAndUI(object):
    """Packages game screen elements"""

    def __init__(self, world_setup):
        self.top_bar = TopBar()
        self.map = Map(world_setup)
        self.world_menu = WorldMenu()

        self.selection = None  # Entity currently being manipulated

    def receive_input(self, curr_input: user_input.Input):
        # todo: cursor selection, unit-menu, unit-cursor
        if self.selection is None:
            pass  # todo
            # self.map.cursor.move(curr_input)
        else:
            self.selection.receive_input(curr_input)


class Tile(object):
    """A square on the map"""

    def __init__(self,
                 tile_terrain: "entities.Terrain",
                 building: typing.Union["entities.Building", "entities.NullEntity"],
                 unit: typing.Union["entities.Unit", "entities.NullEntity"]):
        self.terrain = tile_terrain
        self.building = building
        self.unit = unit


class Cursor(object):
    def __init__(self, world_map: "Map"):
        self.map = world_map
        self.location = points.MapPoint(0, 0)
        self.center()

    def center(self):
        """Center the cursor on the map."""
        self.move_to(points.MapPoint(int(self.map.width / 2), int(self.map.height / 2)))

    def move_direction(self, curr_input: user_input.Input):
        pass  # todo

    def move_to(self, point: points.MapPoint):
        self.location = point
        self.map.scroll_to_cursor()


class Map(object):
    def __init__(self, world_setup: "WorldSetup"):
        self.world_setup = world_setup  # type: WorldSetup
        self._map = self._init_map(
            self.world_setup.map_setup.entity_seed_array)  # type: typing.List[typing.List[Tile]]

        self.size_point = points.ScreenPoint.from_tile(self.width, self.height)
        self.surface = graphics.make_surface(self.size_point.pixel)

        self.cursor = Cursor(self)

    def get_entities(self, layer: typing.Type["layers.Layer"], map_point: points.MapPoint) -> \
            "entities.Entity":
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

    def scroll_to_cursor(self):
        pass  # todo

    def scroll_to_point(self, point):
        """"""

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
        self.surface = sprites.SpriteAnimation("",
                                               "sprites/top_bar").sprite_sheet.original_sprite_sheet_surface


class WorldMenu(object):
    def __init__(self):
        self.surface = sprites.SpriteAnimation("",
                                               "sprites/world_menu").sprite_sheet.original_sprite_sheet_surface


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

        self.map_start_point = points.MapPoint(0, 0)  # type: points.MapPoint
        self.map_end_point = self.map_start_point + self.size_point  # type: points.MapPoint #todo zoom

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
        self.draw_map_surface()

    def draw_map_layer(self, layer: typing.Type[layers.Layer]):
        for x in range(self.viewport.size_point.tile_x):
            for y in range(self.viewport.size_point.tile_y):
                map_point = points.MapPoint.from_tile(x, y)
                self.draw_tile_layer(layer, map_point)

    def draw_tile_layer(self, layer: typing.Type[layers.Layer], map_point: points.MapPoint):
        entity = self.map.get_entities(layer, map_point)
        self.draw_entity_if_not_null_entity(entity, map_point)

    def draw_entity_if_not_null_entity(self, entity: "entities.Entity", map_point: points.MapPoint):
        try:
            self._draw_entity_if_sprite_found(entity, map_point)
        except sprites.DrawNullEntityException:
            pass

    def _draw_entity_if_sprite_found(self, entity: "entities.Entity", map_point: points.MapPoint):
        sprite = entity.sprite
        if sprite:
            self._draw_entity_sprite(sprite, map_point)
        else:
            raise sprites.MissingSpriteException

    def _draw_entity_sprite(self, sprite: pygame.Surface, map_point: points.MapPoint):
        self.map.surface.blit(sprite, map_point.pixel)

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
