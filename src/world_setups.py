import typing
from xml.etree import ElementTree

import armymod
import entities
import layers
import players


class EntitySeed(object):
    """Parameters fed to entity_dict to build an entity"""

    def __init__(self, layer: typing.Type[layers.Layer], army: str, entity: str, player: int):
        self.layer = layer
        self.army = army
        self.entity = entity
        self.player = player


class EntitySeedTile(object):
    def __init__(self,
                 tile_terrain: EntitySeed,
                 building: typing.Optional[EntitySeed],
                 unit: typing.Optional[EntitySeed]):
        self.terrain = tile_terrain
        self.building = building
        self.unit = unit


class MapSetup(object):
    def __init__(self, map_path):
        self._map_path = map_path
        self.xml_tree = ElementTree.parse(self.map_path)
        self.entity_seed_array = self.init_entity_seed_array()

        self.name = self.init_name()
        self.players = self.init_players()  # type: players.PlayerManager

    @property
    def map_path(self):
        return self._map_path

    def init_entity_seed_array(self):
        root = self.xml_tree.getroot()
        entity_seed_array = []
        for column_xml in root.findall("column"):
            column = self._create_column(column_xml)
            entity_seed_array.append(column)

        return entity_seed_array

    def _create_column(self, column_xml: ElementTree.Element):
        tiles = []
        for tile in column_xml:
            tile_xml_terrain = self._xml_element_to_entity_seed(layers.TerrainLayer, tile)
            tile_xml_building = self._xml_element_to_entity_seed(layers.BuildingLayer, tile)
            tile_xml_unit = self._xml_element_to_entity_seed(layers.UnitLayer, tile)

            new_tile = EntitySeedTile(tile_xml_terrain, tile_xml_building, tile_xml_unit)
            tiles.append(new_tile)
        return tiles

    def _xml_element_to_entity_seed(self, layer: typing.Type[layers.Layer],
                                    tile: ElementTree.Element) -> EntitySeed:
        try:
            data = tile.findall(layer.name)[0]
        except IndexError:
            return EntitySeed(layer, "neutral", "null_entity", -1)

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

        return EntitySeed(layer, army, name, int(player))

    def init_name(self):
        try:
            name = self.xml_tree.findall("name")[0].text
            return name
        except IndexError:
            raise ValueError("Map missing name value")

    def init_players(self):
        player_numbers = [-1]
        number_of_players = 0
        for column in self.entity_seed_array:
            for seed in column:
                if seed.building.player not in player_numbers:
                    player_numbers.append(seed.building.player)
                if seed.unit.player not in player_numbers:
                    player_numbers.append(seed.unit.player)
                player_numbers.pop(player_numbers.index(-1))
                number_of_players = len(player_numbers)
        player_manager = players.PlayerManager(number_of_players)
        return player_manager


class WorldSetup(object):
    def __init__(self, map_path):
        self.map_setup = MapSetup(map_path)
        self.armies = armymod.ArmyImporter()
        self.entity_dict = self._initialize_entity_dict()

    @property
    def players(self):
        return self.map_setup.players.player_list

    def _initialize_entity_dict(self):
        entity_dict = {}
        for layer in [layers.TerrainLayer,
                      layers.BuildingLayer,
                      layers.UnitLayer]:
            entity_dict[layer.name] = {}
            entity_dict[layer.name]["neutral"] = {}
            entity_dict[layer.name]["neutral"][
                entities.NullEntity().code_name] = entities.NullEntity

        self._populate_dict_from_terrain(entity_dict)
        for army_plugin in self.armies.plugins:
            army = army_plugin.plugin_object()
            self._populate_dict_from_army(entity_dict, army)

        return entity_dict

    def _populate_dict_from_terrain(self, entity_dict: dict):
        for terrain_type in entities.TERRAIN_LIST:
            entity_dict[layers.TerrainLayer.name]["neutral"][
                terrain_type().code_name] = terrain_type

    def _populate_dict_from_army(self, entity_dict: dict, army: "armymod.Army"):
        entity_dict[layers.BuildingLayer.name][army.code_name] = {}
        for building in army.buildings:
            entity_dict[layers.BuildingLayer.name][army.code_name][building.code_name] = \
                building

        entity_dict[layers.UnitLayer.name][army.code_name] = {}
        for unit in army.units:
            entity_dict[layers.UnitLayer.name][army.code_name][unit.code_name] = unit

    def entity_from_seed(self, entity_seed):
        entity_class = self.access_entity_dict(entity_seed.layer, entity_seed.army,
                                               entity_seed.entity)
        if entity_seed.player == -1:
            entity_instance = entity_class()
        else:
            entity_instance = entity_class(self.players[entity_seed.player])
        return entity_instance

    def access_entity_dict(self, layer: typing.Type[layers.Layer], army: str, entity: str):
        try:
            return self.entity_dict[layer.name][army][entity]
        except KeyError:
            raise KeyError(entity + " not defined. Were they initialized in the army module?")
