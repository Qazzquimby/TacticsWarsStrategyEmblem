class Army(object):
    _name = NotImplemented  # type: str
    _code_name = NotImplemented  # type: str

    def __init__(self):
        pass

    @property
    def name(self) -> str:
        return self._name

    @property
    def code_name(self) -> str:
        return self._code_name
