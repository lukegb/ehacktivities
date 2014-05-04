import datetime

from . import exceptions, utils


class ClubFinances(object):
    def __init__(self, club, year):
        self.club = club
        self.year = year

        self.loaded_data = False

    def __getattr__(self, name):
        if not self.loaded_data:
            for k, v in self.load_data().iteritems():
                setattr(self, k, v)
            self.loaded_data = True
        return super(ClubFinances, self).__getattribute__(name)

    def load_data(self):
        out = {}

        finance_soup, _ = self.club.eactivities.load_and_start(
            '/finance/transactions/{}'.format(self.club.id)
        )

        # pick the correct year
        y = self.club.eactivities.format_year(self.year)
        tab_enc = finance_soup.find(
            "enclosure", label="Transaction Pages Years"
        )
        year_tab = tab_enc.find("tabenclosure", label=y)
        if not year_tab:
            raise ClubFinances.DoesNotExist("Year does not exist")
        if year_tab.attrs['active'] != 'true':
            finance_soup, _ = self.club.eactivities.activate_tab(
                finance_soup, year_tab.attrs['id']
            )

        funding_overview_table = {}
        funding_overview_soup = finance_soup.find("infotable", tableid="658")
        for funding_row_soup in funding_overview_soup.find_all("infotablerow"):
            funding_row_source = unicode(funding_row_soup.find(
                "infotablecell", fieldtype="nvarchar"
            ).get_text())
            funding_row_value = self.club.eactivities.format_price(
                funding_row_soup.find(
                    "infotablecell", fieldtype="float"
                ).get_text()
            )
            funding_overview_table[funding_row_source] = funding_row_value

        out['funding_overview'] = funding_overview_table

        return out

    def banking_records(self):
        return ClubBankingRecords(self)

    class DoesNotExist(exceptions.DoesNotExist):
        pass


class ClubFinancialDocumentation(object):
    document_type = None
    document_name = None

    def __init__(self, club_finances):
        self.club_finances = club_finances

    @property
    def eactivities(self):
        return self.club_finances.club.eactivities

    def optimus_prime(self):
        document_soup, _ = self.eactivities.load_and_start(
            '/finance/documents'
        )

        year_enc = document_soup.find("div", class_="formenc").find(
            "enclosure", recursive=False
        )
        if not year_enc:
            raise exceptions.EActivitiesHasChanged("Can't find year enclosure")

        # choose the correct year
        y = utils.format_year(self.club_finances.year)
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

        # choose the correct document
        dname_enc = dtype_enc.find("enclosure", active="true")
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

        # make sure we're in list mode?
        mode_enc = dname_enc.find("enclosure", active="true")
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

        # now return the soup representing the form enclosure
        return mode_enc.find("enclosure", active="true"), document_soup

    def list(self):
        # here we go
        list_soup, _ = self.optimus_prime()

        items = []
        for row_soup in list_soup.infotable.find_all("infotablerow"):
            items.append(self.parse_list_row(row_soup))

        return items

    def item(self, item_id):
        # yay
        list_soup, document_soup = self.optimus_prime()
        list_enclosure = list_soup.find_parent("enclosure", active="true")
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
            list_enclosure.find("enclosure", label="Details")
        )

    def image(self, item_id, image_id):
        self.item(item_id)
        return self.eactivities.file_handler(image_id)

    def pdf(self, item_id, image_id):
        self.item(item_id)
        return self.eactivities.file_handler(image_id, override=True)

    class DoesNotExist(exceptions.DoesNotExist):
        pass


class ClubBankingRecords(ClubFinancialDocumentation):
    document_type = 'Income'
    document_name = 'Banking Records'

    def parse_list_row(self, row_soup):
        return {
            'id':
                row_soup.find(
                    "infotablecell", alias="Paying in Slip No"
                ).get_text(),
            'gross_amount':
                utils.format_price(
                    row_soup.find(
                        "infotablecell", fieldtype="money"
                    ).get_text()
                )
        }

    def parse_item(self, item_soup):
        data = {}

        _, data['id'] = utils.split_role(
            item_soup.xmlcurrenttitle.get_text()
        )
        data['id'] = int(data['id'])
        data['date'] = datetime.datetime.strptime(
            item_soup.find(
                "infofield", alias="Date Paid In"
            ).get_text(), "%d/%m/%Y"
        ).date()
        data['transaction_lines'] = []

        for tx_line_soup in item_soup.infotable.find_all("infotablerow"):
            tx_line = {}
            tx_line['description'] = tx_line_soup.find(
                "infotablecell", alias="Description"
            ).get_text()
            tx_line['value'] = {}
            tx_line['value']['gross'] = utils.format_price(
                tx_line_soup.find(
                    "infotablecell", fieldtype="money"
                ).get_text()
            )
            tx_line['value']['vat'] = utils.format_vat(
                tx_line_soup.find("infotablecell", alias="VAT Rate").get_text()
            )
            tx_line['value'] = utils.munge_value(tx_line['value'])
            tx_line['account'] = utils.split_account_bracket(
                tx_line_soup.find("infotablecell", alias="Account").get_text()
            )
            tx_line['activity'] = utils.split_account_bracket(
                tx_line_soup.find("infotablecell", alias="Activity").get_text()
            )
            tx_line['funding_source'] = utils.split_account_bracket(
                tx_line_soup.find("infotablecell", alias="Funding").get_text()
            )
            tx_line['consolidation'] = utils.split_account_bracket(
                tx_line_soup.find(
                    "infotablecell", alias="Consolidation"
                ).get_text()
            )

            for k, v in tx_line.iteritems():
                if isinstance(v, unicode):
                    tx_line[k] = unicode(v)

            data['transaction_lines'].append(tx_line)

        data['gross_amount'] = sum([
            x['value']['gross'] for x in data['transaction_lines']
        ])
        data['paying_in_slips'] = [
            unicode(x.get_text()) for x in item_soup.find_all("picture")
        ]

        return data
