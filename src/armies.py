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

"""Classes related to armies.
Actual army implementations are stored as plugins in the plugin folder.
"""

import abc
import typing  # pylint:disable=unused-import

from yapsy.IPlugin import IPlugin

import entities
from importer import Importer  # pylint:disable=no-name-in-module


class Army(abc.ABC):
    """Base class for armies."""
    _name = NotImplemented  # type: str
    _code_name = NotImplemented  # type: str
    _buildings = []  # type: typing.List["entities.Building"]
    _units = []  # type: typing.List["entities.Unit"]

    def __init__(self):
        pass

    @property
    def name(self):
        """str: The army's outwards facing name."""
        return self._name

    @property
    def code_name(self):
        """str: The army's internal name."""
        return self._code_name

    @property
    def buildings(self):
        """List[entities.Building]: Building entities belonging to the army."""
        return self._buildings

    @property
    def units(self):
        """List[entities.Unit]: Unit entities belonging to the army."""
        return self._units

    def add_entity(self, entity):
        """Adds the given entity to the army.

        Args:
            entity (Type[entities.Entity]): The entity to be added.
        """
        if issubclass(entity, entities.Building):  # pylint:disable=no-member
            self._add_building(entity)
        elif issubclass(entity, entities.Unit):  # pylint:disable=no-member
            self._add_unit(entity)
        else:
            raise ValueError

    def _add_building(self, entity):
        self._buildings.append(entity)

    def _add_unit(self, entity):
        self._units.append(entity)


class ArmyPlugin(IPlugin):
    """Empty class to specify that a plugin is an army."""
    pass


class ArmyImporter(Importer):
    """Importer for armies. Reads from the armies directory."""

    def __init__(self):
        Importer.__init__(self, ["../army_plugins"], ArmyPlugin)
