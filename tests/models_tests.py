import unittest

from eactivities.models import Model, DictModel, ArrayModel, LazyModelMixin, LazyDictModel, LazyDictFromArrayModel


class TestSubModel(Model):
    pass


class TestModel(Model):
    _submodels = {
        'xyz': TestSubModel
    }


class TestDictModel(DictModel):
    _submodel = TestSubModel


class TestArrayModel(ArrayModel):
    _submodel = TestSubModel


class ItNeverExistsParser(object):
    def __init__(self, *args, **kwargs):
        pass

    def fetch_data(*args, **kwargs):
        return None


class AlwaysReturnsDictParser(object):
    data = {
        'abc': {'abc': 'def', 'id': 'abc'},
        'mno': {'ghi': 'jkl', 'id': 'mno'},
        'ghi': {'mno': 'pqr', 'id': 'ghi'},
        'xyz': {'xyz': {'aaa': 'bbb'}, 'id': 'xyz'}
    }

    def __init__(self, *args, **kwargs):
        pass

    def fetch_data(self, id=None, *args, **kwargs):
        if id is None:
            return self.data
        return self.data[id]


class AlwaysReturnsListParser(AlwaysReturnsDictParser):
    def fetch_data(self, id=None, *args, **kwargs):
        if id is None:
            return self.data.values()
        return self.data[id]


class TestLazyModel(LazyModelMixin, Model):
    _submodels = {
        'xyz': TestSubModel
    }
    _lazy_loader_parser = AlwaysReturnsDictParser
    _attributes = [
        'abc', 'mno', 'ghi', 'xyz'
    ]


class TestLazyDictModel(LazyDictModel):
    _submodel = TestModel
    _lazy_loader_parser = AlwaysReturnsDictParser


class TestLazyDictFromArrayModel(LazyDictFromArrayModel):
    _submodel = TestModel
    _lazy_loader_parser = AlwaysReturnsListParser


class ModelTestCase(unittest.TestCase):
    def test_model(self):
        m = Model(eactivities=None, parent=None, data={
            'xyz': 'abc',
            'fed': {
                'jkl': 'mno'
            }
        })

        self.assertEqual(m.xyz, 'abc')
        self.assertEqual(m.fed, {'jkl': 'mno'})

    def test_submodelling(self):
        m = TestModel(eactivities=None, parent=None, data={
            'xyz': {
                'jkl': 'mno'
            },
            'abc': 'def'
        })

        self.assertEquals(m.xyz.jkl, 'mno')
        self.assertIsInstance(m.xyz, TestSubModel)


class DictModelTestCase(unittest.TestCase):
    def test_dict_model(self):
        d = {
            'xyz': {
                'abc': 'abc'
            },
            'fed': {
                'add': 'add'
            }
        }
        m = TestDictModel(eactivities=None, parent=None, data=d)

        self.assertEquals(len(m.items()), 2)
        self.assertEquals(len(m.keys()), 2)
        self.assertEquals(len(m.values()), 2)

        self.assertEquals(len(m), len(d))
        for k, v in d.items():
            for ik, iv in v.items():
                self.assertEquals(getattr(m[k], ik), iv)
            self.assertEquals(m[k].dump(), v)


class ArrayModelTestCase(unittest.TestCase):
    def test_array_model(self):
        d = [
            {
                'abc': 'abc'
            },
            {
                'add': 'add'
            }
        ]
        m = TestArrayModel(eactivities=None, parent=None, data=d)

        self.assertEquals(len(m), len(d))
        for i in range(len(d)):
            for k, v in d[i].items():
                self.assertEquals(getattr(m[i], k), v)
            self.assertEquals(m[i].dump(), d[i])


class LazyModelTestCase(unittest.TestCase):
    def test_model(self):
        d = AlwaysReturnsDictParser.data
        m = TestLazyModel(eactivities=None, parent=None, data={})

        # this assertion should go first
        # i.e. make sure submodel processing happens on initial load
        self.assertNotEqual(m.xyz, d['xyz'])

        self.assertEqual(m.abc, d['abc'])
        self.assertEqual(m.mno, d['mno'])
        self.assertEqual(m.ghi, d['ghi'])
        self.assertEqual(m.xyz.xyz, d['xyz']['xyz'])

        self.assertEquals(m.dump(), AlwaysReturnsDictParser.data)

    def test_no_data(self):
        m = TestLazyModel(eactivities=None, parent=None, data={})
        m._lazy_loader_parser = ItNeverExistsParser

        with self.assertRaises(AttributeError):
            m.ddd
        with self.assertRaises(TestLazyModel.DoesNotExist):
            m.abc


class LazyDictModelTestCase(unittest.TestCase):
    def test_dict_model(self):
        m = TestLazyDictModel(eactivities=None, parent=None, data={})

        self.assertEquals(m['abc'].abc, 'def')
        self.assertEquals(m['mno'].ghi, 'jkl')
        self.assertEquals(m['ghi'].mno, 'pqr')
        self.assertEquals(m['xyz'].xyz.aaa, 'bbb')

        with self.assertRaises(KeyError):
            m['ppp']
        with self.assertRaises(AttributeError):
            m['abc'].ghi

        self.assertEquals(m.dump(), AlwaysReturnsDictParser.data)


class LazyDictFromArrayModelTestCase(unittest.TestCase):
    def test_dict_model(self):
        m = TestLazyDictFromArrayModel(eactivities=None, parent=None, data={})

        self.assertEquals(m['abc'].abc, 'def')
        self.assertEquals(m['mno'].ghi, 'jkl')
        self.assertEquals(m['ghi'].mno, 'pqr')
        self.assertEquals(m['xyz'].xyz.aaa, 'bbb')

        with self.assertRaises(KeyError):
            m['ppp']
        with self.assertRaises(AttributeError):
            m['abc'].ghi

        self.assertEquals(m.dump(), AlwaysReturnsDictParser.data.values())
