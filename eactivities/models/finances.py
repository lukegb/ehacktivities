from . import Model, LazyModelMixin, LazyDictFromArrayModel
from eactivities.parsers.finances import FinancesParser, BankingRecordsParser, SalesInvoicesParser, ClaimsParser, PurchaseOrdersParser, \
    TransactionCorrectionsParser, InternalChargesParser, MembersFundsRedistributionsParser, FundingRedistributionsParser


class FinancialDocumentCollection(LazyDictFromArrayModel):
    _submodel = None


class FinancialDocument(LazyModelMixin, Model):
    pass


class BankingRecord(FinancialDocument):
    _lazy_loader_parser = BankingRecordsParser
    _attributes = [
        'id', 'date', 'transaction_lines', 'gross_amount',
        'paying_in_slips'
    ]


class BankingRecords(FinancialDocumentCollection):
    _submodel = BankingRecord
    _lazy_loader_parser = BankingRecordsParser


class SalesInvoice(FinancialDocument):
    _lazy_loader_parser = SalesInvoicesParser
    _attributes = [
        'id', 'date', 'customer', 'customer_purchase_order_number',
        'gross_amount', 'status', 'international', 'audit_trail',
        'next_authorisers', 'transaction_lines', 'purchase_order_attachments',
    ]


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


class Claims(FinancialDocumentCollection):
    _submodel = Claim
    _lazy_loader_parser = ClaimsParser


class PurchaseOrder(FinancialDocument):
    _lazy_loader_parser = PurchaseOrdersParser
    _attributes = [
        'id', 'supplier', 'status', 'payment_date', 'gross_amount',
        'invoice_received', 'finished_goods_receipting', 'pro_forma',
        'audit_trail', 'next_authorisers', 'transaction_lines',
        'gross_amount', 'invoices'
    ]


class PurchaseOrders(FinancialDocumentCollection):
    _submodel = PurchaseOrder
    _lazy_loader_parser = PurchaseOrdersParser


class TransactionCorrection(FinancialDocument):
    _lazy_loader_parser = TransactionCorrectionsParser
    _attributes = [
        'id', 'status', 'gross_amount', 'from_transaction_lines',
        'to_transaction_lines', 'next_authorisers', 'audit_trail'
    ]


class TransactionCorrections(FinancialDocumentCollection):
    _submodel = TransactionCorrection
    _lazy_loader_parser = TransactionCorrectionsParser


class InternalCharge(FinancialDocument):
    _lazy_loader_parser = InternalChargesParser
    _attributes = [
        'id', 'status', 'gross_amount', 'charged_committee', 'receiving_committee',
        'notes', 'audit_trail', 'next_authorisers', 'transaction_lines'
    ]


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


class FundingRedistributions(FinancialDocumentCollection):
    _submodel = FundingRedistribution
    _lazy_loader_parser = FundingRedistributionsParser


class Finances(Model, LazyModelMixin):
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
