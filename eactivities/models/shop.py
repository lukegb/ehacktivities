from . import Model, LazyModelMixin, LazyDictFromArrayModel, ArrayModel, MockModel, Account, Amount, Image
from eactivities.parsers.shop import ShopParser, ShopProductPurchaserParser


class ShopProductPurchaser(Model):
    _attributes = [
        'date', 'order_no', 'cid', 'login',
        'first_name', 'last_name', 'email', 'membership_type'
    ]


class ShopProductPurchaserList(ArrayModel):
    _submodel = ShopProductPurchaser


class ShopProductSKU(Model):
    _submodels = {
        'price': Amount,
        'account': Account,
        'activity': Account
    }

    def purchaser_list(self):
        data = ShopProductPurchaserParser.fetch(
            self._eactivities,
            id=self._parent._parent.id,
            year=self._parent._parent._arguments['year'],
            club_id=self._parent._parent._arguments['club_id'],
            sku_name=self.name
        )

        return ShopProductPurchaserList(eactivities=self._eactivities, parser=ShopProductPurchaserParser, data=data, parent=self)


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

    def purchaser_list(self):
        data = ShopProductPurchaserParser.fetch(self._eactivities, id=self.id, year=self._arguments['year'], club_id=self._arguments['club_id'])

        return ShopProductPurchaserList(eactivities=self._eactivities, parser=ShopProductPurchaserParser, data=data, parent=self)


class ShopProducts(LazyDictFromArrayModel):
    _submodel = ShopProduct
    _lazy_loader_parser = ShopParser


class Shop(MockModel):
    def products(self):
        return ShopProducts(eactivities=self._eactivities, data=self._data, parent=self)
