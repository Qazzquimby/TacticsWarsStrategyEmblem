import entities


class Army(object):
    _name = NotImplemented  #type: str
    _code_name = NotImplemented  #type: str

    def __init__(self):
        pass

    def get_name(self):
        return self._name

    def get_code_name(self):
        return self._code_name
