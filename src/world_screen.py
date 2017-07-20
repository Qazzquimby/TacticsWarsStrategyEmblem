import abc
import typing
from xml.etree import ElementTree as ElementTree

import pygame

import entities
import graphics
import point
import screens
import sprites
import user_input
from point import Location


class Layer(abc.ABC):
    name = NotImplemented  # type: str
    priority = NotImplemented  # type: int


class TerrainLayer(Layer):
    name = "terrain"
    priority = 1


class BuildingLayer(Layer):
    name = "building"
    priority = 2


class UnitLayer(Layer):
    name = "unit"
    priority = 3


class OverlayLayer(Layer):
    name = "overlay"
    priority = 4


class CursorLayer(Layer):
    name = "cursor"
    priority = 5


class MainGameScreen(screens.GameScreen):
    def __init__(self, display, session, world_setup):
        screens.GameScreen.__init__(self, display, session)
        self.world_setup = world_setup
        self.content = MapAndUI(self.world_setup)
        self.animation = MapDrawing(self.content, display)

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
    def __init__(self, tile_terrain: entities.Terrain,
                 building: typing.Union[entities.Building, entities.NullEntity],
                 unit: typing.Union[entities.Unit, entities.NullEntity]):
        self.terrain = tile_terrain
        self.building = building
        self.unit = unit


class Map(object):
    def __init__(self, world_setup: "WorldSetup"):
        self.world_setup = world_setup
        self._map = []
        self._init_map(self.world_setup.map_path)

    def get_entities(self, layer: typing.Type["Layer"], location: Location) -> entities.Entity:
        if layer == TerrainLayer:
            return self.get_terrain(location)
        elif layer == BuildingLayer:
            return self.get_building(location)
        elif layer == UnitLayer:
            return self.get_unit(location)
        else:
            raise TypeError

    def get_terrain(self, location: Location) -> entities.Terrain:
        tile = self.get_tile(location)
        terrain = tile.terrain
        return terrain

    def get_building(self, location: Location) -> entities.Building:
        tile = self.get_tile(location)
        building = tile.building
        return building

    def get_unit(self, location: Location) -> entities.Unit:
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

    def _init_map(self, map_filename: str):
        def parse_map_file(map_filename: str):
            map_xml = ElementTree.parse(map_filename)
            root = map_xml.getroot()
            for column_xml in root:
                column = _create_column(column_xml)
                self._map.append(column)

        def _create_column(column_xml: ElementTree.Element):
            column_list = []
            for tile in column_xml:
                tile_terrain = _xml_to_tile_element(TerrainLayer, tile)
                tile_building = _xml_to_tile_element(BuildingLayer, tile)
                # building_xml = _get_xml_tile_element(tile, BuildingLayer)
                # unit_xml = _get_xml_tile_element(tile, UnitLayer)

                # tile_terrain = entities.Grass()
                # tile_building = entities.NullEntity()
                tile_unit = entities.NullEntity()
                new_tile = Tile(tile_terrain, tile_building, tile_unit)
                column_list.append(new_tile)
            return column_list

        def _xml_to_tile_element(layer: typing.Type[Layer], tile: ElementTree.Element) -> \
                typing.Union[entities.Terrain, entities.Building, entities.Unit]:

            str_army, str_element, player = _xml_element_to_dict_keys(layer, tile)
            tile_element = self.access_entity_dict(layer, str_army, str_element)
            if player == -1:
                tile_element_instance = tile_element() #no player
            else:
                tile_element_instance = tile_element(self.world_setup.players[0]) #fixme, make player
            #  choice dynamic from map xml
            return tile_element_instance

        def _xml_element_to_dict_keys(layer: typing.Type[Layer], tile: ElementTree.Element) -> \
                typing.Tuple[str, str, int]:
            try:
                data = tile.findall(layer.name)[0]
            except IndexError:
                return "neutral", "null_entity", -1

            try:
                army = data.findall("army")[0].text
            except IndexError:
                army = "neutral"  # default when no army given

            try:
                name = data.findall("name")[0].text
            except IndexError:
                name = data.text  # shorthand for neutrals

            try:
                player = data.findall("player")[0].text
            except IndexError:
                player = -1  # shorthand for neutrals

            return army, name, player

        parse_map_file(map_filename)

    def access_entity_dict(self, layer: typing.Type[Layer], army: str, element: str):
        return self.world_setup.entity_dict[layer.name][army][element]


class TopBar(object):
    def __init__(self):
        self.sprite = sprites.SpriteAnimation("", "sprites/top_bar").sprite_sheet.surface


class WorldMenu(object):
    def __init__(self):
        self.sprite = sprites.SpriteAnimation("", "sprites/world_menu").sprite_sheet.surface


class MapDrawing(object):
    def __init__(self, content, display: graphics.Display):
        self.display = display  # type: display.Display
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
        self.draw_map_layer(TerrainLayer)
        self.draw_map_layer(BuildingLayer)
        # todo other layers

    def draw_map_layer(self, layer: typing.Type[Layer]):
        for y in range(self.map.width):
            for x in range(self.map.height):
                location = point.Location(x, y)
                self.draw_tile_layer(layer, location)

    def draw_tile_layer(self, layer: typing.Type[Layer], location: point.Location):
        entity = self.map.get_entities(layer, location)
        self.draw_entity_if_not_null_entity(entity, location)

    def draw_entity_if_not_null_entity(self, entity: entities.Entity, location: point.Location):
        try:
            self._draw_entity_if_sprite_found(entity, location)
        except sprites.DrawNullEntityException:
            pass

    def _draw_entity_if_sprite_found(self, entity: entities.Entity, location: point.Location):
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
