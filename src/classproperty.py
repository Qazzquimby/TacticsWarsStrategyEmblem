class classproperty(object):
    def __init__(self, f):
        self.f = classmethod(f)

    def __get__(self, *a):
        return self.f.__get__(*a)()
