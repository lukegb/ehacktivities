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


class NoneableModelMixin(object):
    pass


class BaseModel(object):
    _submodels = []
    _attributes = []

    def __init__(self, eactivities, data, arguments=None, parent=None, parser=None, *args, **kwargs):
        if data is None and arguments is not None and parser is not None:
            data = parser.fetch(
                eactivities=self._eactivities,
                **arguments
            )
        elif data is None:
            raise RuntimeError("data or (parser and arguments) must be passed!")

        self._data = data
        self._arguments = arguments or {}
        self._parent = parent
        self._eactivities = eactivities
        self._parser = parser

        if parent is not None:
            p = dict(parent._arguments)
            p.update(self._arguments)
            self._arguments = p

        self.load(data)

    class DoesNotExist(exceptions.DoesNotExist):
        pass


class Model(BaseModel):
    def load(self, data):
        for k, v in data.iteritems():
            if k in self._submodels:
                if v is None and issubclass(self._submodels[k], NoneableModelMixin):
                    # v is fine as is...
                    pass
                else:
                    v = self._submodels[k](eactivities=self._eactivities, parser=self._parser, data=v, parent=self)
            setattr(self, k, v)
        self._data.update(**data)

    def dump(self):
        return self._data


class MockModel(BaseModel):
    def load(self, data):
        pass

    def dump(self):
        return {}


class CollectionModelMixin(object):
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


class StringModel(BaseModel):
    def load(self, data):
        pass

    def dump(self):
        return self._data

    def __str__(self):
        return str(self._data)

    def __unicode__(self):
        return unicode(self._data)

    def __repr__(self):
        return repr(self._data)


class ArrayModel(CollectionModelMixin, BaseModel):
    _submodel = None

    def __init__(self, *args, **kwargs):
        self._inner = []

        super(ArrayModel, self).__init__(*args, **kwargs)

    def load(self, data):
        self._inner = []
        for x in data:
            if x is None and issubclass(self._submodels[x], NoneableModelMixin):
                pass
            else:
                x = self._submodel(eactivities=self._eactivities, parser=self._parser, data=x, parent=self)
            self._inner.append(x)

    def dump(self):
        return [x.dump() if x is not None else x for x in self._inner]


class DictModel(CollectionModelMixin, BaseModel):
    _submodel = None
    _dictish = dict

    def __init__(self, *args, **kwargs):
        self._inner = self._dictish()

        super(DictModel, self).__init__(*args, **kwargs)

    def load(self, data):
        i = []
        for k, v in data.iteritems():
            if v is None and issubclass(self._submodels[k], NoneableModelMixin):
                pass
            else:
                v = self._submodel(
                    eactivities=self._eactivities, parser=self._parser, data=v, parent=self
                )
            i.append((k, v))
        self._inner = self._dictish(i)

    def dump(self):
        return self._dictish([(k, v.dump() if v is not None else v) for (k, v) in self._inner.iteritems()])

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
    _lazy_id_attribute = 'id'

    def __init__(self, *args, **kwargs):
        super(LazyModelMixin, self).__init__(*args, **kwargs)

        if isinstance(self._parent, LazyCollectionModelMixin):
            self._arguments[self._parent._lazy_id_attribute] = self._data[self._lazy_id_attribute]

    def perform_lazy_load(self):
        llp = self._lazy_loader_parser(self._eactivities)
        kwargs = dict(self._data)
        if isinstance(self._parent, LazyCollectionModelMixin):
            kwargs[self._parent._lazy_id_attribute] = kwargs[self._lazy_id_attribute]
        data = llp.fetch_data(**kwargs)
        if data is None:
            raise self.DoesNotExist()
        self.load(data)
        self._lazy_loaded = True
        return data

    def __getattr__(self, name):
        if not self._lazy_loaded:
            if name in self._attributes:
                data = self.perform_lazy_load()
                if name in data:
                    # nasty hack to make sure all processing is done!
                    return getattr(self, name)
        raise AttributeError("{} is not an attribute".format(name))


class LazyCollectionModelMixin(CollectionModelMixin):
    LAZY_FICTITIOUS_DATA = {'FICTITIOUS': True}
    _lazy_loader_parser = None
    _lazy_id_attribute = 'id'

    def __init__(self, data=None, *args, **kwargs):
        # Lazy collections are "special"
        # in that the data they are passed
        # contains no actual "data" - just arguments required
        # to fetch the data.
        # We hide the data argument and construct a fictitious one to
        # work around this.
        self._lazy_collection_data = data
        kwargs.setdefault('parser', self._lazy_loader_parser)
        kwargs.setdefault('arguments', data)

        super(LazyCollectionModelMixin, self).__init__(
            data=self.LAZY_FICTITIOUS_DATA, *args, **kwargs
        )

        self._lazy_loaded = False
        self._lazy_load_count = 0
        self._lazy_loader_parser_instance = self._lazy_loader_parser(self._eactivities)

    def load(self, data):
        if data is self.LAZY_FICTITIOUS_DATA:
            # See __init__ comment
            return

        super(LazyCollectionModelMixin, self).load(data)

        for k, v in self._inner.iteritems():
            v._data.update(self._lazy_collection_data)

    @on_access_do_lazy_load
    def dump(self):
        return super(LazyCollectionModelMixin, self).dump()

    def perform_full_lazy_load(self):
        if self._lazy_loaded:
            return self._inner

        data = self._lazy_loader_parser_instance.fetch_data(**self._lazy_collection_data)
        if data is None:
            raise self.DoesNotExist()
        self.load(data)
        self._lazy_loaded = True
        return data

    def retrieve_item(self, key):
        if self._lazy_loaded:
            return self._inner[key]

        self._lazy_load_count += 1
        if self._lazy_load_count > COLLECTION_LAZY_LOAD_THRESHOLD:
            self.perform_full_lazy_load()
            return self._inner[key]

        d = dict(self._lazy_collection_data)
        d[self._lazy_id_attribute] = key

        print d

        data = self._lazy_loader_parser_instance.fetch_data(**d)
        if data is None:
            raise KeyError("No such item")

        return self._submodel(
            eactivities=self._eactivities, arguments={self._lazy_id_attribute: key}, parser=self._parser, data=data, parent=self
        )

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

    def load(self, data):
        if data is self.LAZY_FICTITIOUS_DATA:
            # See __init__ comment
            return

        new_data = self._dictish([(v['id'], v) for v in data])
        super(LazyDictFromArrayModel, self).load(new_data)

    def dump(self):
        return [x.dump() if x is not None else x for x in self._inner.values()]


# LazyArrayModel is a lie


# Now for some generically useful models

class Account(Model):
    pass


class VAT(Model):
    pass


class Amount(Model):
    _submodels = {
        'vat': VAT
    }


class Image(NoneableModelMixin, StringModel):
    _image_id_attribute = 'image_id'

    def retrieve(self):
        self._arguments[self._image_id_attribute] = self._data
        return self._parser(self._eactivities).image(**self._arguments)

    def raw(self):
        self._arguments[self._image_id_attribute] = self._data
        return self._parser(self._eactivities).pdf(**self._arguments)


class Images(ArrayModel):
    _submodel = Image


class PdfableModelMixin(object):
    def pdf(self):
        return self._parser(self._eactivities).item_pdf(**self._arguments)

from .club import Club
__all__ = ['Club']
