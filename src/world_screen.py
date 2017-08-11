import typing

import pygame

import entities
import graphics
import layers
import point
import screens
import sprites
import user_input
from point import Location
from world_setups import WorldSetup


class MainGameScreen(screens.GameScreen):
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
        pass


class MapAndUI(object):
    def __init__(self, world_setup):
        self.top_bar = TopBar()
        self.map = Map(world_setup)
        self.world_menu = WorldMenu()


class Tile(object):
    def __init__(self, tile_terrain: "entities.Terrain",
                 building: typing.Union["entities.Building", "entities.NullEntity"],
                 unit: typing.Union["entities.Unit", "entities.NullEntity"]):
        self.terrain = tile_terrain
        self.building = building
        self.unit = unit


class Map(object):
    def __init__(self, world_setup: "WorldSetup"):
        self.world_setup = world_setup  # type: WorldSetup
        self._map = self._init_map(self.world_setup.map_setup.entity_seed_array)

    def get_entities(self, layer: typing.Type["layers.Layer"], location: Location) -> \
            "entities.Entity":
        if layer == layers.TerrainLayer:
            return self.get_terrain(location)
        elif layer == layers.BuildingLayer:
            return self.get_building(location)
        elif layer == layers.UnitLayer:
            return self.get_unit(location)
        else:
            raise TypeError

    def get_terrain(self, location: Location) -> "entities.Terrain":
        tile = self.get_tile(location)
        terrain = tile.terrain
        return terrain

    def get_building(self, location: Location) -> "entities.Building":
        tile = self.get_tile(location)
        building = tile.building
        return building

    def get_unit(self, location: Location) -> "entities.Unit":
        tile = self.get_tile(location)
        unit = tile.unit
        return unit

    def get_tile(self, location: Location) -> Tile:
        return self._map[location.x][location.y]

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
        self.sprite = sprites.SpriteAnimation("", "sprites/top_bar").sprite_sheet.surface


class WorldMenu(object):
    def __init__(self):
        self.sprite = sprites.SpriteAnimation("", "sprites/world_menu").sprite_sheet.surface


class MapDrawing(object):
    def __init__(self, content, display: graphics.Display):
        self.display = display  # type: graphics.Display
        self.content = content
        self.top_bar = self.content.top_bar
        self.map = content.map
        self.world_menu = content.world_menu

        self.map_larger_than_screen = self._init_map_larger_than_screen()
        self.map_center_offset = self._init_map_center_offset()

    def execute_tick(self):
        self.draw_top_bar()
        self.draw_map()
        self.draw_world_menu()

    def draw_top_bar(self):
        sprite = self.top_bar.sprite
        screen_tile = point.TilePoint(0, 0)
        screen_pixel = screen_tile.to_pixel_point()
        self.display.blit(sprite, screen_pixel)

    def draw_map(self):
        self.draw_map_layer(layers.TerrainLayer)
        self.draw_map_layer(layers.BuildingLayer)
        self.draw_map_layer(layers.UnitLayer)

    def draw_map_layer(self, layer: typing.Type[layers.Layer]):
        for y in range(self.map.width):
            for x in range(self.map.height):
                location = point.Location(x, y)
                self.draw_tile_layer(layer, location)

    def draw_tile_layer(self, layer: typing.Type[layers.Layer], location: point.Location):
        entity = self.map.get_entities(layer, location)
        self.draw_entity_if_not_null_entity(entity, location)

    def draw_entity_if_not_null_entity(self, entity: "entities.Entity", location: point.Location):
        try:
            self._draw_entity_if_sprite_found(entity, location)
        except sprites.DrawNullEntityException:
            pass

    def _draw_entity_if_sprite_found(self, entity: "entities.Entity", location: point.Location):
        sprite = entity.sprite
        if sprite:
            self._draw_entity_sprite(sprite, location)
        else:
            raise sprites.MissingSpriteException

    def _draw_entity_sprite(self, sprite: pygame.Surface, location: point.Location):
        screen_tile = point.TilePoint(location.x + self.map_center_offset.x,
                                      location.y + self.map_center_offset.y +
                                      graphics.TOP_BAR_TILE_HEIGHT)
        screen_pixel = screen_tile.to_pixel_point()

        self.display.blit(sprite, screen_pixel)

    def draw_world_menu(self):
        sprite = self.world_menu.sprite
        menu_top_tile = graphics.TOP_BAR_TILE_HEIGHT + graphics.MAP_TILE_HEIGHT

        screen_tile = point.TilePoint(0, menu_top_tile)
        screen_pixel = screen_tile.to_pixel_point()

        self.display.blit(sprite, screen_pixel)

    def _init_map_larger_than_screen(self) -> bool:
        is_taller = self.map.height > graphics.MAP_TILE_HEIGHT
        is_wider = self.map.width > graphics.MAP_TILE_WIDTH
        is_larger = is_taller or is_wider
        return is_larger

    def _init_map_center_offset(self) -> point.PixelPoint:
        if self.map_larger_than_screen:
            return point.PixelPoint(0, 0)
        else:
            centered_x = int((graphics.MAP_TILE_WIDTH - self.map.width) / 2)
            centered_y = int((graphics.MAP_TILE_HEIGHT - self.map.height) / 2)
            return point.PixelPoint(centered_x, centered_y)
