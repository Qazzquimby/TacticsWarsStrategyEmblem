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

"""Handles reading plugins from the game's plugin directories."""
import abc
import glob
import typing

from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager

from world_setups import WorldSetup


class NoInstanciationPluginManager(PluginManager):
    """A kind of plugin manager that does not instanciate classes it imports."""
    def instanciateElement(self, element):
        """The overwritten plugin manager function. Does not instanciate the element."""
        return element


class ImporterShell(abc.ABC):
    """Importer ABC. Importers handle and hold imported plugins."""

    def __init__(self):
        self.plugins = NotImplemented

    def import_plugins(self):
        """Import function to be overwritten."""
        raise NotImplementedError

    def print_plugins(self):
        """Prints the name of each plugin this contains."""
        for plugin in self.plugins:
            print(plugin.name)


class Importer(ImporterShell):
    """Generic Importer

    Attributes:
        self.manager (NoInstanciationPluginManager): Handles the actual importing.
        self.loocations (List[str]): A list of relative file paths to search for plugins.
        self.plugin_class (Type[IPlugin]): The IPlugin type of class to search for. Plugin
            classes must be specifically defined and passed in.
        self.plugins (List[yapsy.PluginInfo]): The plugins found.
    """

    def __init__(self, locations: typing.List[str], plugin_class: typing.Type[IPlugin]):
        ImporterShell.__init__(self)
        self.manager = NoInstanciationPluginManager()
        self.locations = locations
        self.plugin_class = plugin_class
        self.plugins = self.import_plugins()

    def import_plugins(self):
        """Searches the importer's locations for classes matching the importer's plugin class.
        Returns (List[yapsy.PluginInfo]): The plugins found.
        """
        categories_filter = {"Default": self.plugin_class}
        self.manager.setCategoriesFilter(categories_filter)
        self.manager.setPluginPlaces(self.locations)
        self.manager.collectPlugins()
        return self.manager.getAllPlugins()


class MapImporter(ImporterShell):
    """An importer that collects xml files in the maps directory, and collects them as WorldSetups.
    """

    def __init__(self, locations: typing.List[str]):
        ImporterShell.__init__(self)
        self.locations = locations
        self.plugins = self.import_plugins()

    def import_plugins(self):
        """
        Returns (List[WorldSetup]): A world setup for each xml file found in the maps directory.
        """
        plugins = [WorldSetup(map_path) for map_path in glob.glob('../maps/*.xml')]
        return plugins
