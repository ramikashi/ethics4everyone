from collections import MutableMapping, OrderedDict

class FixedOrderedDict(MutableMapping):
    def __init__(self, *args):
        self._d = OrderedDict(*args)

    def __getitem__(self, key):
        return self._d[key]

    def __setitem__(self, key, value):
        self._d[key] = value

    def __delitem__(self, key):
        del self._d[key]

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)