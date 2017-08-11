import glob
import typing

from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager

from world_setups import WorldSetup


class NoInstanciationPluginManager(PluginManager):
    def instanciateElement(self, element):
        return element


class ImporterShell(object):
    def __init__(self):
        self.plugins = NotImplemented

    def import_plugins(self):
        raise NotImplementedError

    def print_plugins(self):
        for plugin in self.plugins:
            print(plugin.name)


class Importer(ImporterShell):
    def __init__(self, locations: typing.List[str], plugin_class: typing.Type[IPlugin]):
        ImporterShell.__init__(self)
        self.manager = NoInstanciationPluginManager()
        self.locations = locations
        self.plugin_class = plugin_class
        self.plugins = self.import_plugins()

    def import_plugins(self):
        categories_filter = {"Default": self.plugin_class}
        self.manager.setCategoriesFilter(categories_filter)
        self.manager.setPluginPlaces(self.locations)
        self.manager.collectPlugins()
        return self.manager.getAllPlugins()


class MapImporter(ImporterShell):
    def __init__(self, locations: typing.List[str]):
        ImporterShell.__init__(self)
        self.locations = locations
        self.plugins = self.import_plugins()

    def import_plugins(self):
        plugins = [WorldSetup(map_path) for map_path in glob.glob('../maps/*.xml')]
        return plugins
