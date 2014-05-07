from . import Model, ArrayModel, DictModel
from eactivities.parsers.documentation import InventoryParser, KeyListsParser, RiskAssessmentParser


class Documentation(Model):
    def _spawn(self, model_cls, parser_cls):
        return model_cls(
            eactivities=self._eactivities,
            parent=self,
            data=parser_cls.fetch(
                eactivities=self._eactivities,
                club_id=self._data['club_id']
            )
        )

    def inventory(self):
        return self._spawn(Inventory, InventoryParser)

    def risk_assessment(self):
        return self._spawn(RiskAssessment, RiskAssessmentParser)

    def key_lists(self):
        return self._spawn(KeyLists, KeyListsParser)


class InventoryItem(Model):
    pass


class Inventory(ArrayModel):
    _submodel = InventoryItem


class Risk(Model):
    pass


class RiskAssessment(ArrayModel):
    _submodel = Risk


class KeyListPerson(Model):
    pass


class KeyListPeople(ArrayModel):
    _submodel = KeyListPerson


class KeyList(Model):
    _submodels = {
        'people': KeyListPeople
    }


class KeyLists(DictModel):
    _submodel = KeyList
