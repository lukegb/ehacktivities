# vim: set fileencoding=utf-8

import re

from .. import utils, exceptions
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
            return None
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
