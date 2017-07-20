import typing

from yapsy.IPlugin import IPlugin

import entities
from importer import Importer


class Army(object):
    _name = NotImplemented  # type: str
    _code_name = NotImplemented  # type: str
    _buildings = []  # type: typing.List["entities.Building"]
    _units = []  # type: typing.List["entities.Unit"]

    def __init__(self):
        pass

    @property
    def name(self) -> str:
        return self._name

    @property
    def code_name(self) -> str:
        return self._code_name

    @property
    def buildings(self) -> typing.List["entities.Building"]:
        return self._buildings

    @property
    def units(self) -> typing.List["entities.Unit"]:
        return self._units

    def add_entity(self, entity):
        if issubclass(entity, entities.Building):
            self.add_building(entity)
        elif issubclass(entity, entities.Unit):
            self.add_unit(entity)
        else:
            raise ValueError

    def add_building(self, entity):
        self._buildings.append(entity)

    def add_unit(self, entity):
        self._units.append(entity)


class ArmyPlugin(IPlugin):
    pass


class ArmyImporter(Importer):
    def __init__(self):
        Importer.__init__(self, ["../armies"], ArmyPlugin, )