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

"""Handles initializing maps from files."""

import typing
from xml.etree import ElementTree

import armies
import entities
import layers
import players


class EntitySeed(object):
    """Parameters fed to entity_dict to build an entity"""

    def __init__(self, layer, army, entity, player):
        """
        Args:
            layer (layers.Layer class): The layer of the entity.
            army (str): The army of the entity.
            entity (str): The entity's name.
            player (int): The owning player.
        """
        self.layer = layer
        self.army = army
        self.entity = entity
        self.player = player


class EntitySeedTile(object):
    """Contains entity seeds for each main layer of a tile."""

    def __init__(self, terrain, building, unit):
        """
        Args:
            terrain (EntitySeed): The tile's terrain.
            building (Optional(EntitySeed)): The tile's building, if any.
            unit (Optional(EntitySeed)): The tile's unit, if any.
        """
        self.terrain = terrain
        self.building = building
        self.unit = unit


class MapSetup(object):
    """A blueprint of a map.

    Reads from map_path and parses the file.
    Fed to a world_screen.Map for initialization.

    Attributes:
        self.xml_tree (ElementTree): A tree representation of the map file.
        self.entity_seed_grid (list(list(EntitySeedTile))): A 2d grid of entity seed tiles from
            the map file.
        self.name (str): The map name, supplied by the map file.
        self.players (players.PlayerManager): The players present for the map.
    """

    def __init__(self, map_path):
        self._map_path = map_path
        self.xml_tree = ElementTree.parse(self.map_path)
        self.entity_seed_grid = self.init_entity_seed_grid()

        self.name = self.init_name()
        self.players = self.init_players()

    @property
    def map_path(self):
        """str: The relative path to the map file."""
        return self._map_path

    def init_entity_seed_grid(self):
        """Builds the grid of entity seeds from the map's xml representation.

        Returns:
            list(list(EntitySeedTile)): A 2d grid of entity seed tiles, representing the map.
        """
        root = self.xml_tree.getroot()
        entity_seed_grid = []
        for column_xml in root.findall("column"):
            column = self._create_column(column_xml)
            entity_seed_grid.append(column)

        return entity_seed_grid

    def _create_column(self, column_xml):
        """ Builds a single column for the entity seed grid.

        Args:
            column_xml: The relevant column from the map's xml tree.

        Returns:
            list(EntitySeedTile): A column of entity seed tiles.
        """
        tiles = []
        for tile in column_xml:
            tile_xml_terrain = self._xml_element_to_entity_seed(layers.TerrainLayer, tile)
            tile_xml_building = self._xml_element_to_entity_seed(layers.BuildingLayer, tile)
            tile_xml_unit = self._xml_element_to_entity_seed(layers.UnitLayer, tile)

            new_tile = EntitySeedTile(tile_xml_terrain, tile_xml_building, tile_xml_unit)
            tiles.append(new_tile)
        return tiles

    @staticmethod
    def _xml_element_to_entity_seed(layer, tile_xml):
        """Generates the entity seed based on an entity referenced in the map's xml.

        Args:
            layer (Type[layers.Layer]): The layer the entity is on.
            tile_xml (ElementTree.Element): The entity's xml.

        Returns:
            EntitySeed: The generated entity seed.

        """
        try:
            data = tile_xml.findall(layer.name)[0]
        except IndexError:
            return EntitySeed(layer, "neutral", "null_entity", -1)  # entity does not exist

        def get_data(data_name, fallback):
            """Gets the requested information from the entity's data.

            Args:
                data_name (str): The name of the xml element to retrieve.
                fallback (any): The value used if the element is not found.

            Returns:
                Optional(str): The result of the query.
            """
            try:
                result = data.findall(data_name)[0].text
            except IndexError:
                result = fallback

            return result

        army = get_data("army", fallback="neutral")

        name = get_data("name", fallback=data.text)

        player = get_data("player", fallback=-1)  # shorthand for neutral.

        return EntitySeed(layer, army, name, int(player))

    def init_name(self):
        """Gets the map's name from its xml tree.

        Returns:
            str: The map's name.
        """
        try:
            name = self.xml_tree.findall("name")[0].text
            return name
        except IndexError:
            return "Untitled"

    def init_players(self):
        """Generates a player manager for the players present in the map.

        Returns:
            players.PlayerManger: The generated player manager.
        """
        player_numbers = [-1]
        number_of_players = 0
        for column in self.entity_seed_grid:
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
    """A blueprint class for a games session
    Contains the current map_setup object, all imported armies, and a mapping of all entities.
    """

    def __init__(self, map_path):
        """Args:
            map_path (str): The relative path to the map file to be loaded into map_setup.
        """
        self.map_setup = MapSetup(map_path)
        self.armies = armies.ArmyImporter()
        self.entity_dict = self._initialize_entity_dict()

    @property
    def players(self):
        """players.PlayerManager: Holds the players in the game and helpers."""
        return self.map_setup.players

    def _initialize_entity_dict(self):
        """Makes a nested dictionary mapping descriptions to their entity class.
        Dict structure is [layer][army][name]

        Returns:
            dict: The generated dict
        """
        entity_dict = {}
        for layer in [layers.TerrainLayer, layers.BuildingLayer, layers.UnitLayer]:
            entity_dict[layer.name] = {}
            entity_dict[layer.name]["neutral"] = {}
            entity_dict[layer.name]["neutral"][
                entities.NullEntity().code_name] = entities.NullEntity  # pylint: disable=no-member

        self._populate_dict_from_terrain(entity_dict)
        for army_plugin in self.armies.plugins:
            army = army_plugin.plugin_object()
            self._populate_dict_from_army(entity_dict, army)

        return entity_dict

    @staticmethod
    def _populate_dict_from_terrain(entity_dict):
        """Populates the terrain branch of the given entity dict.

        Args:
            entity_dict (dict): The dict to be augmented.
        """
        for terrain_type in entities.TERRAIN_LIST:  # pylint: disable=no-member
            entity_dict[layers.TerrainLayer.name]["neutral"][
                terrain_type().code_name] = terrain_type

    @staticmethod
    def _populate_dict_from_army(entity_dict, army):
        """Populates a given army's branch of the given entity dict.

        Args:
            entity_dict (dict): The dict to be augmented.
            army (Army): The army to add to the dict.
        """
        entity_dict[layers.BuildingLayer.name][army.code_name] = {}
        for building in army.buildings:
            entity_dict[layers.BuildingLayer.name][army.code_name][building.code_name] = building

        entity_dict[layers.UnitLayer.name][army.code_name] = {}
        for unit in army.units:
            entity_dict[layers.UnitLayer.name][army.code_name][unit.code_name] = unit

    def entity_from_seed(self, entity_seed):
        """Gets the entity class from the entity dict, and instantiates it.

        Args:
            entity_seed (EntitySeed): The seed used to fetch the entity.

        Returns:
            entities.Entity: The instantiated entity.

        """
        entity_class = self.access_entity_dict(entity_seed.layer,
                                               entity_seed.army,
                                               entity_seed.entity)
        if entity_seed.player == -1:
            entity_instance = entity_class()
        else:
            entity_instance = entity_class(self.players.player_list[entity_seed.player])
        return entity_instance

    def access_entity_dict(self, layer: typing.Type[layers.Layer], army, entity):
        """Gets the entity class from its mapping in the entity dict

        Args:
            layer (layers.Layer): The layer of the entity.
            army (str): The code name of the entity's army.
            entity (str): The code name of the entity itself.

        Returns:
            Type(Entity): The entity class corresponding with the mappings.
        """
        try:
            return self.entity_dict[layer.name][army][entity]
        except KeyError:
            raise KeyError(
                "{} not defined. Were they initialized in the army module?".format(entity))
