from location import Location
import xml.etree.ElementTree as ElementTree
import entities
import layers
import typing


class MapAndUI(object):
    def __init__(self):
        self.map = Map()


class Tile(object):
    def __init__(self, terrain: entities.Terrain, building: entities.Building,
                 unit: entities.Unit):
        self.terrain = terrain
        self.building = building
        self.unit = unit


class Map(object):
    def __init__(self):
        self._map = []
        self._init_map("../maps/map_filename.xml")

    def get_entities(self, layer: typing.Type[layers.Layer], x, y):
        if layer == layers.TerrainLayer:
            return self.get_terrain(x, y)
        elif layer == layers.BuildingLayer:
            return self.get_building(x, y)
        elif layer == layers.UnitLayer:
            return self.get_unit(x, y)
        else:
            raise TypeError

    def get_terrain(self, x, y) -> entities.Terrain:
        tile = self.get_tile(x, y)
        terrain = tile.terrain
        return terrain

    def get_building(self, x, y) -> entities.Building:
        tile = self.get_tile(x, y)
        building = tile.building
        return building

    def get_unit(self, x, y) -> entities.Unit:
        tile = self.get_tile(x, y)
        unit = tile.unit
        return unit

    def get_tile(self, x, y) -> Tile:
        return self._map[x][y]

    def get_width(self):
        return len(self._map)

    def get_height(self):
        return len(self._map[0])

    def _init_map(self, map_filename):
        CHARACTERS_PER_NAME = 6

        def parse_map_file(map_filename):
            map_xml = ElementTree.parse(map_filename)
            root = map_xml.getroot()
            for column_xml in root:
                column = create_column(column_xml)
                self._map.append(column)

        def create_column(column_xml: ElementTree.Element):
            column_list = []
            for space in column_xml:
                terrain = entities.Grass()
                building = entities.NullEntity()
                unit = entities.NullEntity()
                new_space = Tile(terrain, building, unit)
                column_list.append(new_space)
            return column_list

        parse_map_file(map_filename)
