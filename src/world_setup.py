import entities
import player
import armymod
import world_screen


class WorldSetup(object):
    def __init__(self):
        self._players = []
        self._map_path = "../maps/map_filename.xml"
        self.armies = armymod.ArmyImporter()
        self.entity_dict = self._initialize_entity_dict()

    @property
    def map_path(self):
        return self._map_path

    @property
    def players(self):
        return self._players

    def add_player(self, army: armymod.Army):
        new_player_number = len(self._players)
        new_player = player.Player(new_player_number, army)
        self._players.append(new_player)

        # todo current player
        # todo next player

    def _initialize_entity_dict(self):
        entity_dict = {}
        for layer in [world_screen.TerrainLayer,
                      world_screen.BuildingLayer,
                      world_screen.UnitLayer]:
            entity_dict[layer.name] = {}
            entity_dict[layer.name]["neutral"] = {}
            entity_dict[layer.name]["neutral"][entities.NullEntity().code_name] = entities.NullEntity

        self._populate_dict_from_terrain(entity_dict)
        for army_plugin in self.armies.plugins:
            army = army_plugin.plugin_object()
            self._populate_dict_from_army(entity_dict, army)

        return entity_dict

    def _populate_dict_from_terrain(self, entity_dict: dict):
        for terrain_type in entities.terrain_list:
            entity_dict[world_screen.TerrainLayer.name]["neutral"][
                terrain_type().code_name] = terrain_type

    def _populate_dict_from_army(self, entity_dict: dict, army: armymod.Army):
        entity_dict[world_screen.BuildingLayer.name][army.code_name] = {}
        for building in army.buildings:
            entity_dict[world_screen.BuildingLayer.name][army.code_name][building.code_name] = \
                building

        entity_dict[world_screen.UnitLayer.name][army.code_name] = {}
        #todo same for unit
