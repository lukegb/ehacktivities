class BaseParser(object):
    def __init__(self, eactivities):
        self.eactivities = eactivities

    @classmethod
    def fetch(cls, eactivities, **kwargs):
        return cls(eactivities).fetch_data(**kwargs)
