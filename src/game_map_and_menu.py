from location import Location
import xml.etree.ElementTree as ElementTree
import Entities


class GameMapAndMenu(object):
    def __init__(self):
        self.map = GameMap()


class Tile(object):
    def __init__(self, terrain: Entities.Terrain, building: Entities.Building,
                 unit: Entities.Unit):
        self.terrain = terrain
        self.building = building
        self.unit = unit

class GameMap(object):
    def __init__(self):
        self._map = []
        self._init_map("../maps/map_filename.xml")

    def get_terrain(self, x, y) -> Entities.Terrain:
        tile = self.get_tile(x, y)
        terrain = tile.terrain
        return terrain

    def get_building(self, x, y) -> Entities.Building:
        tile = self.get_tile(x, y)
        building = tile.building
        return building

    def get_unit(self, x, y) -> Entities.Unit:
        tile = self.get_tile(x, y)
        unit = tile.unit
        return unit

    def get_tile(self, x, y) -> Tile:
        return self._map[x][y]

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
                terrain = Entities.Grass()
                building = Entities.NullEntity()
                unit = Entities.NullEntity()
                new_space = Tile(terrain, building, unit)
                column_list.append(new_space)
            return column_list

        parse_map_file(map_filename)



