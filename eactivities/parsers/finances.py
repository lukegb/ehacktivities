# vim: set fileencoding=utf-8

import re

from .. import utils, exceptions
from . import BaseParser

AMOUNT_RE = re.compile(r"Amount \(")
PRICE_RE = re.compile(r"Price .*\(")
TOTAL_RE = re.compile(r"Total .*\(")


class FinancesParser(BaseParser):

    def fetch_data(self, club_id, year):
        out = {}

        finance_soup, _ = self.eactivities.load_and_start(
            '/finance/transactions/{}'.format(club_id)
        )

        # pick the correct year
        y = utils.format_year(year)
        tab_enc = finance_soup.find(
            "enclosure", label="Transaction Pages Years"
        )
        year_tab = tab_enc.find("tabenclosure", label=y)
        if not year_tab:
            return None
        if year_tab.attrs['active'] != 'true':
            self.eactivities.activate_tab(
                finance_soup, year_tab.attrs['id']
            )

        funding_overview_table = {}
        funding_overview_soup = finance_soup.find("infotable", tableid="658")
        for funding_row_soup in funding_overview_soup.find_all("infotablerow"):
            funding_row_source = unicode(funding_row_soup.find(
                "infotablecell", fieldtype="nvarchar"
            ).get_text())
            funding_row_value = utils.format_price(
                funding_row_soup.find(
                    "infotablecell", fieldtype="float"
                ).get_text()
            )
            funding_overview_table[funding_row_source] = funding_row_value

        out['funding_overview'] = funding_overview_table

        return out


class FinancialDocumentationParser(BaseParser):
    document_type = None
    document_name = None

    item_needs_row = False

    def optimus_prime(self, club_id, year):
        document_soup, _ = self.eactivities.load_and_start(
            '/finance/documents/{}'.format(club_id)
        )

        year_enc = document_soup.find("div", class_="formenc").find(
            "enclosure", recursive=False
        )
        if not year_enc:
            raise exceptions.EActivitiesHasChanged("Can't find year enclosure")

        # choose the correct year
        y = utils.format_year(year)
        year_tab = year_enc.find("tabenclosure", label=y)
        if not year_tab:
            raise self.DoesNotExist("Couldn't find year {}".format(y))
        if year_tab.attrs['active'] != 'true':
            self.eactivities.activate_tab(document_soup, year_tab.attrs['id'])

        # choose the correct document type
        dtype_enc = year_enc.find("tabenclosure", active="true")
        if not dtype_enc:
            raise exceptions.EActivitiesHasChanged(
                "Can't find document type enclosure"
            )
        dtype_tab = dtype_enc.find("enclosure", label=self.document_type)
        if not dtype_tab:
            raise self.DoesNotExist(
                "Couldn't find document type '{}'".format(self.document_type)
            )
        if dtype_tab.attrs['active'] != 'true':
            self.eactivities.activate_tab(document_soup, dtype_tab.attrs['id'])
        dtype_tab = dtype_enc.find("enclosure", label=self.document_type)

        # choose the correct document
        dname_enc = dtype_tab
        if not dname_enc:
            raise exceptions.EActivitiesHasChanged(
                "Can't find document enclosure"
            )
        dname_tab = dname_enc.find("enclosure", label=self.document_name)
        if not dname_tab:
            raise self.DoesNotExist(
                "Couldn't find document '{}'".format(self.document_name)
            )
        if dname_tab.attrs['active'] != 'true':
            self.eactivities.activate_tab(document_soup, dname_tab.attrs['id'])
        dname_tab = dname_enc.find("enclosure", label=self.document_name)

        # make sure we're in list mode?
        mode_enc = dname_tab
        if not mode_enc:
            raise exceptions.EActivitiesHasChanged(
                "Can't find list/detail enclosure"
            )
        mode_tab = mode_enc.find("enclosure", label="List")
        if not mode_tab:
            raise exceptions.EActivitiesHasChanged(
                "Couldn't find list mode tab"
            )
        if mode_tab.attrs['active'] != 'true':
            self.eactivities.activate_tab(document_soup, mode_tab.attrs['id'])
        mode_tab = mode_enc.find("enclosure", label="List")

        # now return the soup representing the form enclosure
        return mode_tab, document_soup

    def fetch_data(self, club_id, year, item_id=None, **kwargs):
        if item_id is not None:
            return self.item(club_id, year, item_id)
        return self.list(club_id, year)

    def list(self, club_id, year):
        # here we go
        list_soup, _ = self.optimus_prime(club_id, year)

        if list_soup.find("div", class_="noinfo") is not None:
            # no records
            return []

        items = []
        for row_soup in list_soup.infotable.find_all("infotablerow"):
            items.append(self.parse_list_row(row_soup))

        return items

    def item(self, club_id, year, item_id):
        # yay
        list_soup, document_soup = self.optimus_prime(club_id, year)
        list_enclosure = list_soup.parent
        detail_tab = list_enclosure.find("enclosure", label="Details")
        if not detail_tab:
            raise exceptions.EActivitiesHasChanged(
                "Couldn't find detail mode tab"
            )
        self.eactivities.activate_tab(document_soup, detail_tab.attrs['id'])
        self.eactivities.data_search(
            document_soup, detail_tab.attrs['id'], item_id, tab=True
        )

        if list_soup.find("div", class_="noinfo") is not None:
            # no records
            raise self.DoesNotExist("No document with ID {}".format(item_id))

        row_item = list_enclosure.find("infotablecell", text=unicode(item_id)).find_parent("infotablerow")
        if row_item is None:
            # this item doesn't exist
            raise self.DoesNotExist("No document with ID {}".format(item_id))

        if not self.item_needs_row:
            return self.parse_item(
                list_enclosure.find("enclosure", label="Details")
            )
        else:
            return self.parse_item(
                list_enclosure.find("enclosure", label="Details"),
                row_item
            )

    def parse_audit_trail(self, item_soup):
        audit_trail_label_soup = item_soup.find("label", text='AUDIT TRAIL')
        audit_table_soup = audit_trail_label_soup.find_next_sibling('infotable')
        audit_trail = []

        for audit_row_soup in audit_table_soup.find_all("infotablerow"):
            audit_entry = {}
            audit_entry['role'] = unicode(audit_row_soup.find(
                "infotablecell", alias="Role"
            ).get_text())
            audit_entry['notes'] = unicode(audit_row_soup.find(
                "infotablecell", alias="Notes"
            ).get_text())
            audit_entry['date'] = utils.parse_date(
                audit_row_soup.find(
                    "infotablecell", alias="Date"
                ).get_text()
            )

            person_with_role = audit_entry['notes']
            person_with_role = person_with_role[:person_with_role.find(')) ') + 2]
            person, _ = utils.split_role(person_with_role)
            audit_entry['name'] = person

            audit_trail.append(audit_entry)

        return audit_trail

    def parse_next_authorisers(self, item_soup):
        authorisers_label_soup = item_soup.find("label", text='NEXT AUTHORISERS')
        if not authorisers_label_soup:
            return None

        authorisers_enc_soup = authorisers_label_soup.find_next_sibling('infoenclosure')
        authorisers = []

        for authoriser_row_soup in authorisers_enc_soup.find_all("infofield"):
            authoriser = {}
            authoriser['name'], authoriser['role'] = utils.split_role(
                authoriser_row_soup.get_text()
            )
            authorisers.append(authoriser)

        return authorisers

    class DoesNotExist(exceptions.DoesNotExist):
        pass


class BankingRecordsParser(FinancialDocumentationParser):
    document_type = 'Income'
    document_name = 'Banking Records'

    def parse_list_row(self, row_soup):
        return {
            'id': self.parse_field(row_soup, "Paying in Slip No", cell=True),
            'gross_amount': self.parse_field(row_soup, AMOUNT_RE, 'money', cell=True)
        }

    def parse_item(self, item_soup):
        data = {}

        _, data['id'] = utils.split_role(
            item_soup.xmlcurrenttitle.get_text()
        )
        data['id'] = unicode(data['id'])
        data['date'] = self.parse_field(item_soup, "Date Paid In", 'date')
        data['transaction_lines'] = []

        for tx_line_soup in item_soup.find("infotablehead", text=u'Account').find_parent("infotable").find_all("infotablerow"):
            tx_line = {}
            tx_line['description'] = self.parse_field(tx_line_soup, "Description", cell=True)
            tx_line['value'] = {}
            tx_line['value']['gross'] = self.parse_field(tx_line_soup, AMOUNT_RE, 'money', cell=True)
            tx_line['value']['vat'] = self.parse_field(tx_line_soup, "VAT Rate", 'vat', cell=True)
            tx_line['value'] = utils.munge_value(tx_line['value'])
            tx_line['account'] = self.parse_field(tx_line_soup, "Account", 'account', cell=True)
            tx_line['activity'] = self.parse_field(tx_line_soup, "Activity", 'account', cell=True)
            tx_line['funding_source'] = self.parse_field(tx_line_soup, "Funding", 'account', cell=True)
            tx_line['consolidation'] = self.parse_field(tx_line_soup, "Consolidation", 'account', cell=True)

            data['transaction_lines'].append(tx_line)

        data['gross_amount'] = sum([
            x['value']['gross'] for x in data['transaction_lines']
        ])
        data['paying_in_slips'] = [
            unicode(x.get_text()) for x in item_soup.find_all("picture")
        ]

        return data

    class DoesNotExist(FinancialDocumentationParser.DoesNotExist):
        pass


class SalesInvoicesParser(FinancialDocumentationParser):
    document_type = 'Income'
    document_name = 'Sales Invoices'

    item_needs_row = True

    def parse_list_row(self, row_soup):
        return {
            'id': self.parse_field(row_soup, "Invoice Number", cell=True),
            'date': self.parse_field(row_soup, "Invoice Date", 'date', cell=True),
            'customer': {
                'name': self.parse_field(row_soup, "Customer", cell=True)
            },
            'customer_purchase_order_number': self.parse_field(row_soup, "Purchase Order Number", cell=True),
            'gross_amount': self.parse_field(row_soup, AMOUNT_RE, 'money', cell=True),
            'status': self.parse_field(row_soup, 'Invoice Status', 'status', cell=True),
        }

    def parse_item(self, item_soup, row_soup):
        data = {}

        _, data['id'] = utils.split_role(
            item_soup.xmlcurrenttitle.get_text()
        )
        data['id'] = unicode(data['id'])
        data['date'] = self.parse_field(item_soup, "Invoice Date", 'date')
        data['customer'] = {
            'name': self.parse_field(item_soup, "Customer"),
            'address': self.parse_field(item_soup, "Address"),
            'contact': {
                'name': self.parse_field(item_soup, "Customer Contact Name"),
                'phone': self.parse_field(item_soup, "Customer Contact Phone Number"),
                'email': self.parse_field(item_soup, "Customer Contact Email")
            }
        }
        data['international'] = self.parse_field(item_soup, "International", 'bit')
        data['customer_purchase_order_number'] = self.parse_field(item_soup, "Purchase Order Number")
        data['audit_trail'] = self.parse_audit_trail(item_soup)
        data['next_authorisers'] = self.parse_next_authorisers(item_soup)
        data['transaction_lines'] = []

        data['status'] = self.parse_field(row_soup, 'Invoice Status', 'status', cell=True)

        for tx_line_soup in item_soup.find("infotablehead", text=u'Account').find_parent("infotable").find_all("infotablerow"):
            tx_line = {}
            tx_line['description'] = self.parse_field(tx_line_soup, "Description", cell=True)
            tx_line['quantity'] = self.parse_field(tx_line_soup, "Quantity", 'number', cell=True)

            tx_line['unit_value'] = {}
            tx_line['unit_value']['gross'] = self.parse_field(tx_line_soup, PRICE_RE, 'money', cell=True)
            tx_line['unit_value']['vat'] = self.parse_field(tx_line_soup, "VAT Rate", 'vat', cell=True)
            tx_line['unit_value'] = utils.munge_value(tx_line['unit_value'])

            tx_line['value'] = {}
            tx_line['value']['gross'] = self.parse_field(tx_line_soup, TOTAL_RE, 'money', cell=True)
            tx_line['value']['vat'] = self.parse_field(tx_line_soup, "VAT Rate", 'vat', cell=True)
            tx_line['value'] = utils.munge_value(tx_line['value'])

            tx_line['account'] = self.parse_field(tx_line_soup, "Account", 'account', cell=True)
            tx_line['activity'] = self.parse_field(tx_line_soup, "Activity", 'account', cell=True)
            tx_line['funding_source'] = self.parse_field(tx_line_soup, "Funding", 'account', cell=True)

            data['transaction_lines'].append(tx_line)

        data['gross_amount'] = sum([
            x['value']['gross'] for x in data['transaction_lines']
        ])
        data['purchase_order_attachments'] = [
            unicode(x.get_text()) for x in item_soup.find_all("picture")
        ]

        return data

    def item_pdf(self, item_id, **kwargs):
        # prime $_SESSION
        self.eactivities.load_and_start('/finance/documents')

        # and get the invoice PDF!
        return self.eactivities.streaming_get('/finance/documents/invoices/pdf/%s' % (unicode(item_id),))

    class DoesNotExist(FinancialDocumentationParser.DoesNotExist):
        pass


class ClaimsParser(FinancialDocumentationParser):
    document_type = 'Expenditure'
    document_name = 'Claims'

    def parse_list_row(self, row_soup):
        return {
            'id': self.parse_field(row_soup, "Claim Number", cell=True),
            'person': self.parse_field(row_soup, "Person", cell=True),
            'status': self.parse_field(row_soup, "Claim Status", 'status', cell=True),
            'payment_date': self.parse_field(row_soup, "Payment Date", "date", cell=True),
            'gross_amount': self.parse_field(row_soup, AMOUNT_RE, "money", cell=True)
        }

    def parse_item(self, item_soup):
        data = {}

        _, data['id'] = utils.split_role(
            item_soup.xmlcurrenttitle.get_text()
        )
        data['id'] = unicode(data['id'])
        data['payment_date'] = self.parse_field(item_soup, "Payment Date", "date")
        data['person'] = self.parse_field(item_soup, "Person")
        data['notes'] = self.parse_field(item_soup, "Notes")
        data['gross_amount'] = self.parse_field(item_soup, AMOUNT_RE, 'money')
        data['status'] = self.parse_field(item_soup, "Claim Status", 'status')
        data['audit_trail'] = self.parse_audit_trail(item_soup)
        data['next_authorisers'] = self.parse_next_authorisers(item_soup)
        data['transaction_lines'] = []

        for tx_line_soup in item_soup.find("infotablehead", text=u'Account').find_parent("infotable").find_all("infotablerow"):
            tx_line = {}
            tx_line['description'] = self.parse_field(tx_line_soup, "Description", cell=True)
            tx_line['value'] = {}
            tx_line['value']['gross'] = self.parse_field(tx_line_soup, PRICE_RE, 'money', cell=True)
            tx_line['value']['vat'] = self.parse_field(tx_line_soup, "VAT Rate", 'vat', cell=True)
            tx_line['value'] = utils.munge_value(tx_line['value'])
            tx_line['account'] = self.parse_field(tx_line_soup, "Account", 'account', cell=True)
            tx_line['activity'] = self.parse_field(tx_line_soup, "Activity", 'account', cell=True)
            tx_line['funding_source'] = self.parse_field(tx_line_soup, "Funding", 'account', cell=True)
            tx_line['consolidation'] = self.parse_field(tx_line_soup, "Consolidation", 'account', cell=True)

            data['transaction_lines'].append(tx_line)

        data['receipts'] = [
            unicode(x.get_text()) for x in item_soup.find_all("picture")
        ]

        return data

    class DoesNotExist(FinancialDocumentationParser.DoesNotExist):
        pass


class PurchaseOrdersParser(FinancialDocumentationParser):
    document_type = 'Expenditure'
    document_name = 'Purchase Orders'

    item_needs_row = True

    def parse_list_row(self, row_soup):
        return {
            'id': self.parse_field(row_soup, "Order Number", cell=True),
            'supplier': {'name': self.parse_field(row_soup, "Supplier", cell=True)},
            'status': self.parse_field(row_soup, "Order Status", 'status', cell=True),
            'payment_date': self.parse_field(row_soup, "Payment Date", 'date', cell=True),
            'gross_amount': self.parse_field(row_soup, AMOUNT_RE, 'money', cell=True),
            'invoice_received': self.parse_field(row_soup, "Invoice Received", 'bit', cell=True),
            'finished_goods_receipting': self.parse_field(row_soup, "Finished Goods Receipting", 'bit', cell=True),
            'pro_forma': self.parse_field(row_soup, "Pro Forma", 'bit', cell=True),
        }

    def parse_item(self, item_soup, row_soup):
        data = {}

        _, data['id'] = utils.split_role(
            item_soup.xmlcurrenttitle.get_text()
        )
        data['id'] = unicode(data['id'])
        data['payment_date'] = self.parse_field(item_soup, "Payment Date", 'date')
        data['supplier'] = {
            'name': self.parse_field(item_soup, "Supplier"),
            'address': self.parse_field(item_soup, "Address")
        }
        data['status'] = self.parse_field(item_soup, "Order Status", 'status')
        data['audit_trail'] = self.parse_audit_trail(item_soup)
        data['next_authorisers'] = self.parse_next_authorisers(item_soup)
        data['transaction_lines'] = []

        data['invoice_received'] = self.parse_field(item_soup, "Invoice Received", 'bit')
        data['finished_goods_receipting'] = self.parse_field(item_soup, "Finished Goods Receipting", 'bit')

        # pro formas are also only obvious from the list (I think)
        # there's probably some way you can tell from the details page
        # but I don't have any pro formas to test with
        data['pro_forma'] = self.parse_field(row_soup, "Pro Forma", 'bit', cell=True)

        for tx_line_soup in item_soup.find("infotablehead", text=u'Account').find_parent("infotable").find_all("infotablerow"):
            tx_line = {}
            tx_line['description'] = self.parse_field(tx_line_soup, "Description", cell=True)

            tx_line['unit_value'] = {}
            tx_line['unit_value']['gross'] = self.parse_field(tx_line_soup, PRICE_RE, 'money', cell=True)
            tx_line['unit_value']['vat'] = self.parse_field(tx_line_soup, "VAT Rate", 'vat', cell=True)
            tx_line['unit_value'] = utils.munge_value(tx_line['unit_value'])

            tx_line['value'] = {}
            tx_line['value']['gross'] = self.parse_field(tx_line_soup, TOTAL_RE, 'money', cell=True)
            tx_line['value']['vat'] = self.parse_field(tx_line_soup, "VAT Rate", 'vat', cell=True)
            tx_line['value'] = utils.munge_value(tx_line['value'])

            tx_line['account'] = self.parse_field(tx_line_soup, "Account", 'account', cell=True)
            tx_line['activity'] = self.parse_field(tx_line_soup, "Activity", 'account', cell=True)
            tx_line['funding_source'] = self.parse_field(tx_line_soup, "Funding", 'account', cell=True)
            tx_line['consolidation'] = self.parse_field(tx_line_soup, "Consolidation", 'account', cell=True)

            tx_line['quantity'] = {
                'ordered': self.parse_field(tx_line_soup, "Quantity", 'number', cell=True),
                'received': self.parse_field(tx_line_soup, "Number Received", 'number', cell=True),
            }

            for k, v in tx_line.iteritems():
                if isinstance(v, unicode):
                    tx_line[k] = unicode(v)

            data['transaction_lines'].append(tx_line)

        data['gross_amount'] = sum([
            x['value']['gross'] for x in data['transaction_lines']
        ])
        data['invoices'] = [
            unicode(x.get_text()) for x in item_soup.find_all("picture")
        ]

        return data

    def item_pdf(self, item_id, **kwargs):
        # prime the session
        self.eactivities.load_and_start('/finance/documents')

        # and get the PO PDF!
        return self.eactivities.streaming_get('/finance/documents/orders/pdf/%d' % (item_id,))

    class DoesNotExist(FinancialDocumentationParser.DoesNotExist):
        pass


class TransactionCorrectionsParser(FinancialDocumentationParser):
    document_type = 'Transfers'
    document_name = 'Transaction Corrections'

    def parse_list_row(self, row_soup):
        return {
            'id': self.parse_field(row_soup, "Correction Number", cell=True),
            'status': self.parse_field(row_soup, "Correction Status", 'status', cell=True),
            'gross_amount': self.parse_field(row_soup, AMOUNT_RE, "money", cell=True)
        }

    def parse_item(self, item_soup):
        # we need the "to" transaction lines!
        from_enclosure = item_soup.find("enclosure", label="From Lines")
        to_enclosure = item_soup.find("enclosure", label="To Lines")
        self.eactivities.activate_tab(item_soup, to_enclosure.attrs['id'])

        data = {}

        _, data['id'] = utils.split_role(
            item_soup.xmlcurrenttitle.get_text()
        )
        data['id'] = unicode(data['id'])

        data['gross_amount'] = self.parse_field(item_soup, AMOUNT_RE, 'money')
        data['status'] = self.parse_field(item_soup, "Correction Status", 'status')

        data['audit_trail'] = self.parse_audit_trail(item_soup)
        data['next_authorisers'] = self.parse_next_authorisers(item_soup)

        data['from_transaction_lines'] = []
        data['to_transaction_lines'] = []

        for tx_line_soup in from_enclosure.find_all("infotablerow"):
            tx_line = {}
            tx_line['description'] = self.parse_field(tx_line_soup, "Description", cell=True)

            tx_line['value'] = {}
            tx_line['value']['gross'] = self.parse_field(tx_line_soup, AMOUNT_RE, 'money', cell=True)
            tx_line['value'] = utils.munge_value(tx_line['value'])

            tx_line['account'] = self.parse_field(tx_line_soup, "Account", 'account', cell=True)
            tx_line['activity'] = self.parse_field(tx_line_soup, "Activity", 'account', cell=True)
            tx_line['funding_source'] = self.parse_field(tx_line_soup, "Funding", 'account', cell=True)

            data['from_transaction_lines'].append(tx_line)

        for tx_line_soup in to_enclosure.find_all("infotablerow"):
            tx_line = {}
            tx_line['description'] = self.parse_field(tx_line_soup, "Description", cell=True)

            tx_line['value'] = {}
            tx_line['value']['gross'] = self.parse_field(tx_line_soup, AMOUNT_RE, 'money', cell=True)
            tx_line['value'] = utils.munge_value(tx_line['value'])

            tx_line['account'] = self.parse_field(tx_line_soup, "Account", 'account', cell=True)
            tx_line['activity'] = self.parse_field(tx_line_soup, "Activity", 'account', cell=True)
            tx_line['funding_source'] = self.parse_field(tx_line_soup, "Funding", 'account', cell=True)

            data['to_transaction_lines'].append(tx_line)

        return data

    class DoesNotExist(FinancialDocumentationParser.DoesNotExist):
        pass


class FundingRedistributionsParser(FinancialDocumentationParser):
    document_type = 'Transfers'
    document_name = 'Funding Redistributions'

    def parse_list_row(self, row_soup):
        return {
            'id': self.parse_field(row_soup, "Redistribution", cell=True),
            'funding_source': self.parse_field(row_soup, "Funding", 'account', cell=True),
            'status': self.parse_field(row_soup, "Redistribution Status", 'status', cell=True),
            'gross_amount': self.parse_field(row_soup, AMOUNT_RE, "money", cell=True)
        }

    def parse_item(self, item_soup):
        # we need the "to" transaction lines!
        from_enclosure = item_soup.find("enclosure", label="From Lines")
        to_enclosure = item_soup.find("enclosure", label="To Lines")
        self.eactivities.activate_tab(item_soup, to_enclosure.attrs['id'])

        data = {}

        _, data['id'] = utils.split_role(
            item_soup.xmlcurrenttitle.get_text()
        )
        data['id'] = unicode(data['id'])

        data['funding_source'] = self.parse_field(item_soup, "Funding", 'account')
        data['gross_amount'] = self.parse_field(item_soup, AMOUNT_RE, 'money')

        data['status'] = self.parse_field(item_soup, "Redistribution Status", 'status')

        data['audit_trail'] = self.parse_audit_trail(item_soup)
        data['next_authorisers'] = self.parse_next_authorisers(item_soup)

        data['from_transaction_lines'] = []
        data['to_transaction_lines'] = []

        for tx_line_soup in from_enclosure.find_all("infotablerow"):
            tx_line = {}
            tx_line['description'] = self.parse_field(tx_line_soup, "Description", cell=True)

            tx_line['value'] = {}
            tx_line['value']['gross'] = self.parse_field(tx_line_soup, AMOUNT_RE, 'money', cell=True)
            tx_line['value'] = utils.munge_value(tx_line['value'])

            tx_line['account'] = self.parse_field(tx_line_soup, "Account", 'account', cell=True)
            tx_line['activity'] = self.parse_field(tx_line_soup, "Activity", 'account', cell=True)

            data['from_transaction_lines'].append(tx_line)

        for tx_line_soup in to_enclosure.find_all("infotablerow"):
            tx_line = {}
            tx_line['description'] = self.parse_field(tx_line_soup, "Description", cell=True)

            tx_line['value'] = {}
            tx_line['value']['gross'] = self.parse_field(tx_line_soup, AMOUNT_RE, 'money', cell=True)
            tx_line['value'] = utils.munge_value(tx_line['value'])

            tx_line['account'] = self.parse_field(tx_line_soup, "Account", 'account', cell=True)
            tx_line['activity'] = self.parse_field(tx_line_soup, "Activity", 'account', cell=True)

            data['to_transaction_lines'].append(tx_line)

        return data

    class DoesNotExist(FinancialDocumentationParser.DoesNotExist):
        pass


class MembersFundsRedistributionsParser(FinancialDocumentationParser):
    document_type = 'Transfers'
    document_name = 'Members Funds Redistributions'

    item_needs_row = True

    def parse_list_row(self, row_soup):
        return {
            'id': self.parse_field(row_soup, "Redistribution", cell=True),
            'person': self.parse_field(row_soup, "Person", cell=True),
            'status': self.parse_field(row_soup, "Redistribution Status", 'status', cell=True),
            'funding_source': self.parse_field(row_soup, "Funding", 'account', cell=True),
            'gross_amount': self.parse_field(row_soup, AMOUNT_RE, "money", cell=True)
        }

    def parse_item(self, item_soup, row_soup):
        # we need the "to" transaction lines!
        from_enclosure = item_soup.find("enclosure", label="From Lines")
        to_enclosure = item_soup.find("enclosure", label="To Lines")
        self.eactivities.activate_tab(item_soup, to_enclosure.attrs['id'])

        data = {}

        _, data['id'] = utils.split_role(
            item_soup.xmlcurrenttitle.get_text()
        )
        data['id'] = unicode(data['id'])

        data['person'] = self.parse_field(item_soup, "Person")
        data['funding_source'] = self.parse_field(item_soup, "Funding", 'account')
        data['gross_amount'] = self.parse_field(item_soup, AMOUNT_RE, 'money')
        data['notes'] = self.parse_field(item_soup, "Notes")

        data['status'] = self.parse_field(row_soup, "Redistribution Status", 'status', cell=True)

        data['audit_trail'] = self.parse_audit_trail(item_soup)
        data['next_authorisers'] = self.parse_next_authorisers(item_soup)

        data['from_transaction_lines'] = []
        data['to_transaction_lines'] = []

        for tx_line_soup in from_enclosure.find_all("infotablerow"):
            tx_line = {}
            tx_line['description'] = self.parse_field(tx_line_soup, "Description", cell=True)

            tx_line['value'] = {}
            tx_line['value']['gross'] = self.parse_field(tx_line_soup, AMOUNT_RE, 'money', cell=True)
            tx_line['value'] = utils.munge_value(tx_line['value'])

            tx_line['account'] = self.parse_field(tx_line_soup, "Account", 'account', cell=True)
            tx_line['activity'] = self.parse_field(tx_line_soup, "Activity", 'account', cell=True)

            data['from_transaction_lines'].append(tx_line)

        for tx_line_soup in to_enclosure.find_all("infotablerow"):
            tx_line = {}
            tx_line['description'] = self.parse_field(tx_line_soup, "Description", cell=True)

            tx_line['value'] = {}
            tx_line['value']['gross'] = self.parse_field(tx_line_soup, AMOUNT_RE, 'money', cell=True)
            tx_line['value'] = utils.munge_value(tx_line['value'])

            tx_line['account'] = self.parse_field(tx_line_soup, "Account", 'account', cell=True)
            tx_line['activity'] = self.parse_field(tx_line_soup, "Activity", 'account', cell=True)

            data['to_transaction_lines'].append(tx_line)

        return data

    class DoesNotExist(FinancialDocumentationParser.DoesNotExist):
        pass


class InternalChargesParser(FinancialDocumentationParser):
    document_type = 'Transfers'
    document_name = 'Internal Charges'

    def list(self, club_id, year):
        # here we go
        list_soup, document_soup = self.optimus_prime(club_id, year)

        if list_soup.find("div", class_="noinfo") is not None:
            # no records
            return []

        charged_enclosure = list_soup.find_parent("enclosure")
        charging_enclosure = charged_enclosure.find_next_sibling("enclosure")

        # expand the charging enclosure while we're at it
        self.eactivities.activate_tab(document_soup, charging_enclosure.attrs['id'])

        nice_name = unicode(charged_enclosure.attrs['label'])
        nice_name = nice_name[:nice_name.find(" Charged")]
        self.club_ident = {
            'id': unicode(club_id),
            'name': nice_name,
        }

        items = []
        for row_soup in charged_enclosure.find_all("infotablerow"):
            items.append(self.parse_list_row(row_soup, False))
        for row_soup in charging_enclosure.find_all("infotablerow"):
            items.append(self.parse_list_row(row_soup, True))

        return items

    def item(self, club_id, year, item_id):
        # yay
        list_soup, document_soup = self.optimus_prime(club_id, year)

        charged_enclosure = list_soup.find_parent("enclosure")
        charging_enclosure = charged_enclosure.find_next_sibling("enclosure")

        nice_name = unicode(charged_enclosure.attrs['label'])
        nice_name = nice_name[:nice_name.find(" Charged")]
        self.club_ident = {
            'id': unicode(club_id),
            'name': nice_name,
        }

        # let's check to see if we can find the item in "this" list
        item_entry = charged_enclosure.find(alias="Charge Number", text=unicode(item_id))
        if item_entry is None:
            # expand the charging enclosure
            self.eactivities.activate_tab(document_soup, charging_enclosure.attrs['id'])
            item_entry = charging_enclosure.find(alias="Charge Number", text=unicode(item_id))

        if item_entry is None:
            raise self.DoesNotExist("No document with ID {}".format(item_id))

        list_enclosure = item_entry.find_parent("enclosure", label="List").parent
        detail_tab = list_enclosure.find("enclosure", label="Details")
        if not detail_tab:
            raise exceptions.EActivitiesHasChanged(
                "Couldn't find detail mode tab"
            )
        self.eactivities.activate_tab(document_soup, detail_tab.attrs['id'])
        self.eactivities.data_search(
            document_soup, detail_tab.attrs['id'], item_id, tab=True
        )

        return self.parse_item(
            list_enclosure.find("enclosure", label="Details"),
            item_entry.find_parent("infotablerow")
        )

    def parse_list_row(self, row_soup, charging):
        other_committee_column = 'Receiving Committee' if not charging else 'Charged Committee'
        other_committee = {}
        other_committee['name'], other_committee['id'] = utils.split_role(
            self.parse_field(row_soup, other_committee_column, cell=True)
        )

        receiving_committee = self.club_ident if charging else other_committee
        charged_committee = other_committee if charging else self.club_ident

        return {
            'id': self.parse_field(row_soup, "Charge Number", cell=True),
            'status': self.parse_field(row_soup, "Charge Status", 'status', cell=True),
            'gross_amount': self.parse_field(row_soup, AMOUNT_RE, "money", cell=True),
            'charged_committee': charged_committee,
            'receiving_committee': receiving_committee
        }

    def parse_item(self, item_soup, item_entry):
        data = {}

        _, data['id'] = utils.split_role(
            item_soup.xmlcurrenttitle.get_text()
        )
        data['id'] = unicode(data['id'])

        receiving_committee = self.parse_field(item_soup, "Receiving Committee")
        committee_being_charged = self.parse_field(item_soup, "Committee Being Charged")
        if receiving_committee:
            data['receiving_committee'] = rc = {}
            rc['name'], rc['id'] = utils.split_role(receiving_committee)
            data['charged_committee'] = self.club_ident
        else:
            data['charged_committee'] = cc = {}
            cc['name'], cc['id'] = utils.split_role(committee_being_charged)
            data['receiving_committee'] = self.club_ident

        # this isn't exposed in the "Details" view for some reason.
        # why? I don't know.
        # it's just how it works.
        data['status'] = self.parse_field(item_entry, "Charge Status", 'status', cell=True)

        data['gross_amount'] = self.parse_field(item_soup, AMOUNT_RE, 'money')
        data['notes'] = self.parse_field(item_soup, "Notes")

        data['audit_trail'] = self.parse_audit_trail(item_soup)
        data['next_authorisers'] = self.parse_next_authorisers(item_soup)

        data['transaction_lines'] = []

        for tx_line_soup in item_soup.find("infotablehead", text=u'Account').find_parent("infotable").find_all("infotablerow"):
            tx_line = {}
            tx_line['description'] = self.parse_field(tx_line_soup, "Description", cell=True)

            tx_line['value'] = {}
            tx_line['value']['gross'] = self.parse_field(tx_line_soup, AMOUNT_RE, 'money', cell=True)
            tx_line['value'] = utils.munge_value(tx_line['value'])

            tx_line['account'] = self.parse_field(tx_line_soup, "Account", 'account', cell=True)
            tx_line['activity'] = self.parse_field(tx_line_soup, "Activity", 'account', cell=True)
            tx_line['funding_source'] = self.parse_field(tx_line_soup, "Funding", 'account', cell=True)

            data['transaction_lines'].append(tx_line)

        return data

    class DoesNotExist(FinancialDocumentationParser.DoesNotExist):
        pass
