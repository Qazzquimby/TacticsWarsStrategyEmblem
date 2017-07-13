import xml.etree.ElementTree as ElementTree

import entities
import layers
import sprites
from point import Location
import typing
import terrain
import ironlegion
from world_setup import WorldSetup


class MapAndUI(object):
    def __init__(self, world_setup):
        self.top_bar = TopBar()
        self.map = Map(world_setup)
        self.world_menu = WorldMenu()


class Tile(object):
    def __init__(self, tile_terrain: terrain.Terrain,
                 building: typing.Union[entities.Building, entities.NullEntity],
                 unit: typing.Union[entities.Unit, entities.NullEntity]):
        self.terrain = tile_terrain
        self.building = building
        self.unit = unit


class Map(object):
    def __init__(self, world_setup: WorldSetup):
        self.world_setup = world_setup
        self._map = []
        self._init_map(self.world_setup.map_path)

    def get_entities(self, layer: typing.Type[layers.Layer], location: Location) -> entities.Entity:
        if layer == layers.TerrainLayer:
            return self.get_terrain(location)
        elif layer == layers.BuildingLayer:
            return self.get_building(location)
        elif layer == layers.UnitLayer:
            return self.get_unit(location)
        else:
            raise TypeError

    def get_terrain(self, location: Location) -> terrain.Terrain:
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
        def parse_map_file(map_filename):
            map_xml = ElementTree.parse(map_filename)
            root = map_xml.getroot()
            for column_xml in root:
                column = create_column(column_xml)
                self._map.append(column)

        def create_column(column_xml: ElementTree.Element):
            column_list = []
            for tile in column_xml:
                tile_terrain = terrain.Grass()
                tile_building = ironlegion.HQ(self.world_setup._players[0],
                                              self.world_setup._players[
                                                  0].army)  # fixme use the xml ???
                tile_unit = entities.NullEntity()
                new_tile = Tile(tile_terrain, tile_building, tile_unit)
                column_list.append(new_tile)
            return column_list

        parse_map_file(map_filename)


class TopBar(object):
    def __init__(self):
        self.sprite = sprites.SpriteAnimation("", "sprites/top_bar").sprite_sheet.surface


class WorldMenu(object):
    def __init__(self):
        self.sprite = sprites.SpriteAnimation("", "sprites/world_menu").sprite_sheet.surface
