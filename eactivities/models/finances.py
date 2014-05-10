from . import Model, LazyModelMixin, LazyDictFromArrayModel, ArrayModel, Account, Amount, Images, PdfableModelMixin, NoneableModelMixin
from eactivities.parsers.finances import FinancesParser, BankingRecordsParser, SalesInvoicesParser, ClaimsParser, PurchaseOrdersParser, \
    TransactionCorrectionsParser, InternalChargesParser, MembersFundsRedistributionsParser, FundingRedistributionsParser


class TransactionLine(Model):
    _submodels = {
        'value': Amount,
        'unit_value': Amount,
        'account': Account,
        'activity': Account,
        'funding_source': Account,
        'consolidation': Account
    }


class TransactionLineSet(ArrayModel):
    _submodel = TransactionLine


class AuditEntry(Model):
    pass


class AuditTrail(ArrayModel):
    _submodel = AuditEntry


class Authoriser(Model):
    pass


class NextAuthorisers(NoneableModelMixin, Model):
    pass


class FinancialDocumentCollection(LazyDictFromArrayModel):
    _submodel = None
    _lazy_id_attribute = 'item_id'


class FinancialDocument(LazyModelMixin, Model):
    pass


class BankingRecord(FinancialDocument):
    _lazy_loader_parser = BankingRecordsParser
    _attributes = [
        'id', 'date', 'transaction_lines', 'gross_amount',
        'paying_in_slips'
    ]
    _submodels = {
        'transaction_lines': TransactionLineSet,
        'paying_in_slips': Images
    }


class BankingRecords(FinancialDocumentCollection):
    _submodel = BankingRecord
    _lazy_loader_parser = BankingRecordsParser


class SalesInvoice(PdfableModelMixin, FinancialDocument):
    _lazy_loader_parser = SalesInvoicesParser
    _attributes = [
        'id', 'date', 'customer', 'customer_purchase_order_number',
        'gross_amount', 'status', 'international', 'audit_trail',
        'next_authorisers', 'transaction_lines', 'purchase_order_attachments',
    ]
    _submodels = {
        'transaction_lines': TransactionLineSet,
        'next_authorisers': NextAuthorisers,
        'purchase_order_attachments': Images
    }


class SalesInvoices(FinancialDocumentCollection):
    _submodel = SalesInvoice
    _lazy_loader_parser = SalesInvoicesParser


class Claim(FinancialDocument):
    _lazy_loader_parser = ClaimsParser
    _attributes = [
        'id', 'person', 'status', 'payment_date', 'gross_amount',
        'notes', 'audit_trail', 'next_authorisers', 'transaction_lines',
        'receipts'
    ]
    _submodels = {
        'transaction_lines': TransactionLineSet,
        'next_authorisers': NextAuthorisers,
        'receipts': Images
    }


class Claims(FinancialDocumentCollection):
    _submodel = Claim
    _lazy_loader_parser = ClaimsParser


class PurchaseOrder(PdfableModelMixin, FinancialDocument):
    _lazy_loader_parser = PurchaseOrdersParser
    _attributes = [
        'id', 'supplier', 'status', 'payment_date', 'gross_amount',
        'invoice_received', 'finished_goods_receipting', 'pro_forma',
        'audit_trail', 'next_authorisers', 'transaction_lines',
        'gross_amount', 'invoices'
    ]
    _submodels = {
        'transaction_lines': TransactionLineSet,
        'next_authorisers': NextAuthorisers,
        'invoices': Images
    }


class PurchaseOrders(FinancialDocumentCollection):
    _submodel = PurchaseOrder
    _lazy_loader_parser = PurchaseOrdersParser


class TransactionCorrection(FinancialDocument):
    _lazy_loader_parser = TransactionCorrectionsParser
    _attributes = [
        'id', 'status', 'gross_amount', 'from_transaction_lines',
        'to_transaction_lines', 'next_authorisers', 'audit_trail'
    ]
    _submodels = {
        'from_transaction_lines': TransactionLineSet,
        'to_transaction_lines': TransactionLineSet,
        'next_authorisers': NextAuthorisers
    }


class TransactionCorrections(FinancialDocumentCollection):
    _submodel = TransactionCorrection
    _lazy_loader_parser = TransactionCorrectionsParser


class InternalCharge(FinancialDocument):
    _lazy_loader_parser = InternalChargesParser
    _attributes = [
        'id', 'status', 'gross_amount', 'charged_committee', 'receiving_committee',
        'notes', 'audit_trail', 'next_authorisers', 'transaction_lines'
    ]
    _submodels = {
        'transaction_lines': TransactionLineSet,
        'next_authorisers': NextAuthorisers
    }


class InternalCharges(FinancialDocumentCollection):
    _submodel = InternalCharge
    _lazy_loader_parser = InternalChargesParser


class MembersFundsRedistribution(FinancialDocument):
    _lazy_loader_parser = MembersFundsRedistributionsParser
    _attributes = [
        'id', 'status', 'person', 'from_transaction_lines',
        'to_transaction_lines', 'next_authorisers', 'audit_trail',
        'funding_source', 'gross_amount'
    ]
    _submodels = {
        'from_transaction_lines': TransactionLineSet,
        'to_transaction_lines': TransactionLineSet,
        'next_authorisers': NextAuthorisers
    }


class MembersFundsRedistributions(FinancialDocumentCollection):
    _submodel = MembersFundsRedistribution
    _lazy_loader_parser = MembersFundsRedistributionsParser


class FundingRedistribution(FinancialDocument):
    _lazy_loader_parser = FundingRedistributionsParser
    _attributes = [
        'id', 'status', 'gross_amount', 'funding_source',
        'audit_trail', 'next_authorisers', 'from_transaction_lines',
        'to_transaction_lines'
    ]
    _submodels = {
        'from_transaction_lines': TransactionLineSet,
        'to_transaction_lines': TransactionLineSet,
        'next_authorisers': NextAuthorisers
    }


class FundingRedistributions(FinancialDocumentCollection):
    _submodel = FundingRedistribution
    _lazy_loader_parser = FundingRedistributionsParser


class Finances(LazyModelMixin, Model):
    _lazy_loader_parser = FinancesParser
    _attributes = [
        'funding_overview'
    ]

    # Income #
    def banking_records(self):
        return self._spawn(BankingRecords, BankingRecordsParser)

    def sales_invoices(self):
        return self._spawn(SalesInvoices, SalesInvoicesParser)
    # TODO: Credit Notes

    # Expenditure #
    def claims(self):
        return self._spawn(Claims, ClaimsParser)

    def purchase_orders(self):
        return self._spawn(PurchaseOrders, PurchaseOrdersParser)
    # TODO: Imprests, Credit Card Requests, Charitable Donations

    # Transfers #
    def transaction_corrections(self):
        return self._spawn(TransactionCorrections, TransactionCorrectionsParser)

    def internal_charges(self):
        return self._spawn(InternalCharges, InternalChargesParser)

    def members_funds_redistributions(self):
        return self._spawn(MembersFundsRedistributions, MembersFundsRedistributionsParser)

    def funding_redistributions(self):
        return self._spawn(FundingRedistributions, FundingRedistributionsParser)
    # TODO: Designated Members Funds Transfers

    def _spawn(self, model_cls, parser_cls):
        return model_cls(
            eactivities=self._eactivities,
            parent=self,
            data=dict(
                club_id=self._data['club_id'],
                year=self._data['year']
            )
        )
