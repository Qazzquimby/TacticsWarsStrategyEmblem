import abc

import world_screen


class Command(abc.ABC):
    def __init__(self, target, content: "world_screen.MapAndUI"):
        self.target = target
        self.content = content

    def execute(self):
        raise NotImplementedError
