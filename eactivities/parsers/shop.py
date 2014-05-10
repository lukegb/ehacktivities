# vim: set fileencoding=utf-8

import re
import decimal

from .. import utils, exceptions, encoding_utils
from . import BaseParser

AMOUNT_RE = re.compile(r"Amount \(")
PRICE_RE = re.compile(r"Price .*\(")
TOTAL_RE = re.compile(r"Total .*\(")

SOMETHING_SUBMITTED_PRODUCTS = re.compile(r".+ Submitted Products")


class ShopParser(BaseParser):
    def fetch_data(self, club_id, year, id=None):
        if id is not None:
            return self.item(club_id, year, id)
        return self.list(club_id, year)

    def optimus_prime(self, club_id, year):
        document_soup, _ = self.eactivities.load_and_start(
            '/finance/income/shop/{}'.format(club_id)
        )

        if document_soup.find("xmlcurrenttitle", text="NO RECORDS") is not None:
            raise exceptions.AccessDenied("NO RECORDS found on page")

        committee_box_soup = document_soup.find("insertfield", attrs={'name': 'Committee'})
        if committee_box_soup is None:
            raise exceptions.EActivitiesHasChanged("Can't find Committee text box")
        _, got_club_id = utils.split_role(committee_box_soup.attrs['value'])
        if unicode(got_club_id) != unicode(club_id):
            raise exceptions.AccessDenied("Access denied - found club {}, expected {}".format(got_club_id, club_id))

        # Edit Submitted Products
        esp_soup = document_soup.find("enclosure", label="Edit Submitted Products")
        if not esp_soup:
            raise exceptions.EActivitiesHasChanged("Can't find Edit Submitted Products")
        if esp_soup.attrs['active'] != 'true':
            self.eactivities.activate_tab(document_soup, esp_soup.attrs['id'])
            esp_soup = document_soup.find("enclosure", label="Edit Submitted Products")

        # <club> Submitted Products
        csp_soup = esp_soup.find("enclosure", label=SOMETHING_SUBMITTED_PRODUCTS)
        if not csp_soup:
            raise exceptions.EActivitiesHasChanged("Can't find <club> Submitted Products")
        if csp_soup.attrs['active'] != 'true':
            self.eactivities.activate_tab(document_soup, csp_soup.attrs['id'])
            csp_soup = esp_soup.find("enclosure", label=SOMETHING_SUBMITTED_PRODUCTS)

        # <year>
        y = utils.format_year(year)
        year_soup = csp_soup.find("tabenclosure", label=y)
        if not year_soup:
            raise exceptions.YearNotAvailable()
        if year_soup.attrs['active'] != 'true':
            self.eactivities.activate_tab(document_soup, year_soup.attrs['id'])
            year_soup = csp_soup.find("tabenclosure", label=y)

        # list
        list_soup = year_soup.find("enclosure", label="List")
        if not list_soup:
            raise exceptions.EActivitiesHasChanged("Can't find List")
        if list_soup.attrs['active'] != 'true':
            self.eactivities.activate_tab(document_soup, list_soup.attrs['id'])
            list_soup = year_soup.find("enclosure", label="List")

        return list_soup, document_soup

    def list(self, club_id, year):
        list_soup, _ = self.optimus_prime(club_id, year)

        out = []
        for row_soup in list_soup.find_all("infotablerow"):
            out.append(self.parse_row(row_soup))

        return out

    def parse_row(self, row_soup):
        name, product_id = utils.split_role(self.parse_field(row_soup, 'Product Name', 'text', cell=True))
        return {
            'id': product_id,
            'name': name,
            'submitted_by': self.parse_field(row_soup, 'Submitted By', 'text', cell=True),
            'product_type': self.remove_gumpf_and_caps(self.parse_field(row_soup, 'Product Type', 'text', cell=True)),
            'sale_period': {
                'start': self.parse_field(row_soup, 'Selling Start Date', 'datetime', cell=True),
                'end': self.parse_field(row_soup, 'Selling End Date', 'datetime', cell=True),
            },
            'transferred': self.parse_field(row_soup, 'Transferred', 'bit', cell=True),
            'inactive': self.parse_field(row_soup, 'Inactive', 'bit', cell=True),
        }

    def remove_gumpf_and_caps(self, text):
        if not text or ' - ' not in text:
            return text

        out, _, _ = text.partition(' - ')
        return out.upper()

    def item(self, club_id, year, item_id):
        list_soup, document_soup = self.optimus_prime(club_id, year)

        search_re = re.compile(r".* \(" + str(item_id) + r"\)")
        if list_soup.find("infotablecell", text=search_re) is None:
            raise self.DoesNotExist("No such item {}".format(search_re))

        list_enclosure = list_soup.parent
        detail_tab = list_enclosure.find("enclosure", label="Details")
        if not detail_tab:
            raise exceptions.EActivitiesHasChanged("Couldn't find Detail tab")
        self.eactivities.activate_tab(document_soup, detail_tab.attrs['id'])
        self.eactivities.data_search(
            document_soup, detail_tab.attrs['id'], item_id, tab=True
        )

        if list_soup.find("div", class_="noinfo") is not None:
            # no records
            raise self.DoesNotExist("No item with ID {}".format(item_id))

        row_item = list_enclosure.find("infotablecell", text=search_re).find_parent("infotablerow")
        if row_item is None:
            # this item doesn't exist
            raise self.DoesNotExist("No item with ID {}".format(item_id))

        return self.parse_item(
            list_enclosure.find("enclosure", label="Details"),
            row_item
        )

    def parse_item(self, item_soup, row_soup):
        out = self.parse_row(row_soup)

        # load the Product Image data too
        product_image_tab_soup = item_soup.find("enclosure", label="Product Image")
        self.eactivities.activate_tab(item_soup, product_image_tab_soup.attrs['id'])
        product_image_tab_soup = item_soup.find("enclosure", label="Product Image")

        # add display type, description, max purchases, page order and SKUs
        out['display_type'] = self.parse_field(item_soup, 'Display Type', 'text', form=True).split(' ')[0].upper()
        out['description'] = self.parse_field(item_soup, 'Description', 'text', form=True)
        out['max_purchases_per_person'] = self.parse_field(item_soup, 'Max Purchases per Person', 'int', form=True)
        out['page_order'] = self.parse_field(item_soup, 'Page Order', 'int', form=True)

        # try and get the Product Image
        current_image = product_image_tab_soup.find("picture", persistant="1")
        out['product_image'] = current_image.get_text() if current_image else None

        out['skus'] = []
        for sku_soup in item_soup.find("enclosure", label="Product Lines").find_all("recordrow"):
            out['skus'].append({
                'id': unicode(sku_soup.attrs['id']),
                'name': self.parse_field(sku_soup, 'Name', 'text', form=True),
                'account': self.parse_field(sku_soup, 'Account', 'account', form=True),
                'activity': self.parse_field(sku_soup, 'Activity', 'account', form=True),
                'price': utils.munge_value({
                    'gross': self.parse_field(sku_soup, PRICE_RE, 'money', form=True),
                    'vat': self.parse_field(sku_soup, 'VAT Rate', 'vat', form=True),
                }),
                'quantity': self.parse_field(sku_soup, 'Quantity', 'int', form=True),
                'unlimited_quantity': self.parse_field(sku_soup, 'Unlimited Quantity', 'bit', form=True),
                'requires_collection': self.parse_field(sku_soup, 'Requires Collection?', 'bit', form=True),
            })

        return out

    class DoesNotExist(exceptions.DoesNotExist):
        pass


class ShopProductPurchaserParser(BaseParser):
    def optimus_prime(self, club_id, year):
        document_soup, _ = self.eactivities.load_and_start(
            '/finance/income/shop/{}'.format(club_id)
        )

        if document_soup.find("xmlcurrenttitle", text="NO RECORDS") is not None:
            raise exceptions.AccessDenied("NO RECORDS found on page")

        committee_box_soup = document_soup.find("insertfield", attrs={'name': 'Committee'})
        if committee_box_soup is None:
            raise exceptions.EActivitiesHasChanged("Can't find Committee text box")
        _, got_club_id = utils.split_role(committee_box_soup.attrs['value'])
        if unicode(got_club_id) != unicode(club_id):
            raise exceptions.AccessDenied("Access denied")

        # Purchases Summary
        ps_soup = document_soup.find("enclosure", label="Purchases Summary")
        if not ps_soup:
            raise exceptions.EActivitiesHasChanged("Can't find Purchases Summary")
        if ps_soup.attrs['active'] != 'true':
            self.eactivities.activate_tab(document_soup, ps_soup.attrs['id'])
            ps_soup = document_soup.find("enclosure", label="Purchases Summary")

        # Purchase Reports
        pr_soup = ps_soup.find("enclosure", label="Purchase Reports")
        if not pr_soup:
            raise exceptions.EActivitiesHasChanged("Can't find Purchase Reports")
        if pr_soup.attrs['active'] != 'true':
            self.eactivities.activate_tab(document_soup, pr_soup.attrs['id'])
            pr_soup = ps_soup.find("enclosure", label="Purchase Reports")

        # <year>
        y = utils.format_year(year)
        year_soup = ps_soup.find("tabenclosure", label=y)
        if not year_soup:
            raise exceptions.YearNotAvailable()
        if year_soup.attrs['active'] != 'true':
            self.eactivities.activate_tab(document_soup, year_soup.attrs['id'])
            year_soup = ps_soup.find("tabenclosure", label=y)

        return year_soup, document_soup

    def fetch_data(self, club_id, year, id, sku_name=None):
        data = ShopParser(self.eactivities).fetch_data(club_id, year, id)

        product_name = data['name']

        if sku_name is not None:
            for sku in data['skus']:
                if sku['name'] == sku_name:
                    break
            else:
                raise self.DoesNotExist("Unable to find SKU")

        year_soup, document_soup = self.optimus_prime(club_id, year)

        # find the infotable
        product_table_soup = year_soup.find("infotable", title=product_name)
        if not product_table_soup:
            raise exceptions.EActivitiesHasChanged("Unable to locate table on Purchase Reports page")

        if sku_name is None:
            # if we're doing the product and not an SKU, handle it now
            return self.handle_csv(product_table_soup.attrs['linkobj'])

        # otherwise, keep going to find the SKU
        sku_row_soup = product_table_soup.find("infotablecell", text=sku_name)
        if not sku_row_soup:
            raise exceptions.EActivitiesHasChanged("Unable to locate row on Purchase Reports page")
        sku_row_soup = sku_row_soup.find_parent("infotablerow")

        return self.handle_csv(sku_row_soup.find("infotablecell", alias="Download").attrs['linkobj'])

    def handle_csv(self, relative_url):
        relative_url = '/' + relative_url

        # download the csv!
        resp = self.eactivities.streaming_get(relative_url)
        csvr = encoding_utils.EActivitiesDictCsvReader(resp.raw)

        out = []
        for row in csvr:
            data = {
                'date': utils.parse_date(row['Date']),
                'order_no': row['Order No'],
                'cid': row['CID/Card Number'],
                'login': row['Login'],
                'first_name': row['First Name'],
                'last_name': row['Last Name'],
                'email': row['Email'],
                'product_name': row['Product Name'],
                'unit_price': {
                    'gross': decimal.Decimal(row['Unit Price'])
                },
                'quantity': {
                    'ordered': None if row['Quantity'] == '' else int(row['Quantity']),
                    'collected': None if row['Quantity Collected'] == '' else int(row['Quantity Collected'])
                },
                'price': {
                    'gross': decimal.Decimal(row['Gross Price'])
                }
            }
            out.append(data)

        return out
