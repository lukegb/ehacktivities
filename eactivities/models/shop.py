from . import Model, LazyModelMixin, LazyDictFromArrayModel, ArrayModel, MockModel, Account, Amount, Image
from eactivities.parsers.shop import ShopParser


class ShopProductSKU(Model):
    _submodels = {
        'price': Amount,
        'account': Account,
        'activity': Account
    }


class ShopProductSKUs(ArrayModel):
    _submodel = ShopProductSKU


class SalePeriod(Model):
    _attributes = ['start', 'end']


class ShopProduct(LazyModelMixin, Model):
    _attributes = [
        'id', 'name', 'submitted_by', 'sale_period',
        'transferred', 'inactive', 'description',
        'page_order', 'max_purchases_per_person',
        'product_image', 'skus'
    ]
    _submodels = {
        'skus': ShopProductSKUs,
        'sale_period': SalePeriod,
        'product_image': Image
    }


class ShopProducts(LazyDictFromArrayModel):
    _submodel = ShopProduct
    _lazy_loader_parser = ShopParser


class Shop(MockModel):
    def products(self):
        return ShopProducts(eactivities=self._eactivities, data=self._data, parent=self)
