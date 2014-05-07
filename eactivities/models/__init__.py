import functools
from collections import OrderedDict

from .. import exceptions


COLLECTION_LAZY_LOAD_THRESHOLD = 4


def on_access_do_lazy_load(f):
    @functools.wraps(f)
    def inner(self, *args, **kwargs):
        if not self._lazy_loaded:
            self.perform_full_lazy_load()
        return f(self, *args, **kwargs)
    return inner


class BaseModel(object):
    _submodels = []
    _attributes = []

    def __init__(self, eactivities, data, parent=None, *args, **kwargs):
        self._data = data
        self._parent = parent
        self._eactivities = eactivities

        self.load_data(data)

    class DoesNotExist(exceptions.DoesNotExist):
        pass


class Model(BaseModel):
    def load_data(self, data):
        for k, v in data.iteritems():
            if k in self._submodels:
                v = self._submodels[k](eactivities=self._eactivities, data=v, parent=self)
            setattr(self, k, v)


class CollectionModelMixin(object):
    def __init__(self, data, *args, **kwargs):
        super(CollectionModelMixin, self).__init__(data={}, *args, **kwargs)

    def __len__(self):
        return len(self._inner)

    def __getitem__(self, key):
        return self._inner[key]

    def __setitem__(self, key, value):
        raise TypeError("Not allowed")

    def __delitem__(self, key):
        raise TypeError("Not allowed")

    def __iter__(self):
        return iter(self._inner)

    def __reversed__(self):
        return reversed(self._inner)

    def __contains__(self, item):
        return item in self._inner

    def __str__(self):
        return str(self._inner)

    def __unicode__(self):
        return unicode(self._inner)

    def __repr__(self):
        return repr(self._inner)


class ArrayModel(CollectionModelMixin, BaseModel):
    _submodel = None

    def __init__(self, *args, **kwargs):
        self._inner = []

        super(ArrayModel, self).__init__(*args, **kwargs)

    def load_data(self, data):
        self._inner = [self._submodel(eactivities=self._eactivities, data=x, parent=self) for x in data]


class DictModel(CollectionModelMixin, BaseModel):
    _submodel = None
    _dictish = dict

    def __init__(self, *args, **kwargs):
        self._inner = self._dictish()

        super(DictModel, self).__init__(*args, **kwargs)

    def load_data(self, data):
        self._inner = self._dictish([(k, self._submodel(eactivities=self._eactivities, data=v, parent=self)) for k, v in data.iteritems()])

    def items(self):
        return self._inner.items()

    def keys(self):
        return self._inner.keys()

    def values(self):
        return self._inner.values()


class LazyModelMixin(object):
    _lazy_loader_parser = None
    _attributes = []
    _lazy_loaded = False

    def perform_lazy_load(self):
        llp = self._lazy_loader_parser(self._eactivities)
        data = llp.fetch_data(**self._data)
        if data is None:
            raise self.DoesNotExist()
        self.load_data(data)
        self._lazy_loaded = True
        return data

    def __getattr__(self, name):
        if not self._lazy_loaded:
            if name in self._attributes:
                data = self.perform_lazy_load()
                if name in data:
                    return data[name]
        raise AttributeError("{} is not an attribute".format(name))


class LazyCollectionModelMixin(CollectionModelMixin):
    LAZY_FICTITIOUS_DATA = {'FICTITIOUS': True}
    _lazy_loader_parser = None

    def __init__(self, data=None, *args, **kwargs):
        # Lazy collections are "special"
        # in that the data they are passed
        # contains no actual "data" - just arguments required
        # to fetch the data.
        # We hide the data argument and construct a fictitious one to
        # work around this.
        self._lazy_collection_data = data

        super(LazyCollectionModelMixin, self).__init__(data=self.LAZY_FICTITIOUS_DATA, *args, **kwargs)

        self._lazy_loaded = False
        self._lazy_load_count = 0
        self._lazy_loader_parser_instance = self._lazy_loader_parser(self._eactivities)

    def load_data(self, data):
        if data is self.LAZY_FICTITIOUS_DATA:
            # See __init__ comment
            return

        super(LazyCollectionModelMixin, self).load_data(data)

        for k, v in self._inner.iteritems():
            v._data.update(self._lazy_collection_data)

    def perform_full_lazy_load(self):
        if self._lazy_loaded:
            return self._inner

        data = self._lazy_loader_parser_instance.fetch_data(**self._lazy_collection_data)
        if data is None:
            raise self.DoesNotExist()
        self.load_data(data)
        self._lazy_loaded = True
        return data

    def retrieve_item(self, key):
        if self._lazy_loaded:
            return self._inner[key]

        self._lazy_load_count += 1
        if self._lazy_load_count > COLLECTION_LAZY_LOAD_THRESHOLD:
            self.perform_full_lazy_load()
            return self._inner[key]

        data = self._lazy_loader_parser_instance.fetch_data(id=key, **self._lazy_collection_data)
        if data is None:
            raise KeyError("No such item")

        return self._submodel(eactivities=self._eactivities, data=data, parent=self)

    @on_access_do_lazy_load
    def __len__(self):
        return super(LazyCollectionModelMixin, self).__len__()

    def __getitem__(self, key):
        if not self._lazy_loaded:
            return self.retrieve_item(key)
        return self._inner[key]

    @on_access_do_lazy_load
    def __iter__(self):
        return super(LazyCollectionModelMixin, self).__iter__()

    @on_access_do_lazy_load
    def __reversed__(self):
        return super(LazyCollectionModelMixin, self).__reversed__()

    @on_access_do_lazy_load
    def __contains__(self, item):
        return super(LazyCollectionModelMixin, self).__contains__()

    @on_access_do_lazy_load
    def __str__(self):
        return super(LazyCollectionModelMixin, self).__str__()

    @on_access_do_lazy_load
    def __unicode__(self):
        return super(LazyCollectionModelMixin, self).__unicode__()

    @on_access_do_lazy_load
    def __repr__(self):
        return super(LazyCollectionModelMixin, self).__repr__()


class LazyDictModel(LazyCollectionModelMixin, DictModel):

    @on_access_do_lazy_load
    def items(self):
        return self._inner.items()

    @on_access_do_lazy_load
    def keys(self):
        return self._inner.keys()

    @on_access_do_lazy_load
    def values(self):
        return self._inner.values()


class LazyDictFromArrayModel(LazyDictModel):
    """
    This class does special-sauce conversion of arrays->dicts
    when it loads them.

    i.e. this makes a Parser that returns an Array create a model which
    is referenced like a dictionary!

    Magical! :)
    """

    _dictish = OrderedDict

    def load_data(self, data):
        new_data = self._dictish([(v['id'], v) for v in data])
        super(LazyDictFromArrayModel, self).load_data(new_data)


# LazyArrayModel is a lie

from .club import Club
__all__ = ['Club']
