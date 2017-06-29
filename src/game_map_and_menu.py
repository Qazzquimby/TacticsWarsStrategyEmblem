from location import Location
import xml.etree.ElementTree as ElementTree
import Entities


class GameMapAndMenu(object):
    def __init__(self):
        map = GameMap()


class GameMap(object):
    def __init__(self):
        self._map = [[]]
        self._init_map("../maps/map_filename.xml")

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
                new_space = Space(terrain, building, unit)
                column_list.append(new_space)
            return column_list

        parse_map_file(map_filename)


class Space(object):
    def __init__(self, terrain: Entities.Entity, building: Entities.Entity, unit: Entities.Entity):
        self.terrain = terrain
        self.building = building
        self.unit = unit
