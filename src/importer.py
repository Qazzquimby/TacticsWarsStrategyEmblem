import typing

from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager


class NoInstanciationPluginManager(PluginManager):
    def instanciateElement(self, element):
        return element


class Importer(object):
    def __init__(self, locations: typing.List[str], plugin_class: typing.Type[IPlugin]):
        self.manager = NoInstanciationPluginManager()
        self.locations = locations
        self.plugin_class = plugin_class
        self.plugins = self.import_plugins()
        self.print_plugins()

    def import_plugins(self):
        categories_filter = {"Default": self.plugin_class}
        self.manager.setCategoriesFilter(categories_filter)
        self.manager.setPluginPlaces(self.locations)
        self.manager.collectPlugins()
        return self.manager.getAllPlugins()

    def print_plugins(self):
        for plugin in self.plugins:
            print(plugin.name)
