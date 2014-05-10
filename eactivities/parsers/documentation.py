# vim: set fileencoding=utf-8

import re

from .. import utils, exceptions
from . import BaseParser

EXEMPT_RE = re.compile("Exempt from")


class RecordDocumentParser(BaseParser):
    document_name = None
    column_map = {}

    def optimus_prime(self, club_id):
        document_soup, _ = self.eactivities.load_and_start(
            '/admin/csp/documents/{}'.format(club_id)
        )

        if document_soup.find("xmlcurrenttitle", text="NO RECORDS") is not None:
            raise exceptions.AccessDenied("NO RECORDS found on page")

        main_soup = document_soup.find("div", class_="formenc")
        enc_tab = main_soup.find("enclosure", label=self.document_name)
        if enc_tab.attrs['active'] != 'true':
            self.eactivities.activate_tab(document_soup, enc_tab.attrs['id'])

        return enc_tab, document_soup

    def is_exempt(self, enc_tab):
        return enc_tab.find("formtext", text=EXEMPT_RE) is not None

    def list(self, club_id):
        enc_tab, _ = self.optimus_prime(club_id)

        if self.is_exempt(enc_tab):
            return None

        output = []

        for record in enc_tab.find_all("recordrow"):
            output.append(self.handle_record(record))

        return output

    def process_value(self, value, name, stated_type):
        dispatch = {
            'field': unicode,
            'int': lambda x: None if not x else int(x),
            'lookup': unicode,
            'money': utils.format_price,
            'date': utils.parse_date,
            'checkbox': bool
        }

        return dispatch[stated_type](value)

    def handle_record(self, record):
        out = {}

        out['id'] = record.attrs['id']

        for field in record.find_all("field"):
            field_name = field.attrs['name']
            field_value = field.attrs['value']

            # trim any stuff off the end
            if ' (' in field_name:
                field_name = field_name[:field_name.find(" (")]

            if field_name not in self.column_map:
                continue

            field_value = self.process_value(field_value, field_name, field.attrs['type'])

            output_name = self.column_map[field_name]
            split_output_name = output_name.split('.')
            if len(split_output_name) > 1:
                operating = out
                for segment in split_output_name[:-1]:
                    operating = operating.setdefault(segment, {})
                operating[split_output_name[-1]] = field_value
            else:
                out[output_name] = field_value

        return out

    def fetch_data(self, club_id, **kwargs):
        return self.list(club_id)


class InventoryParser(RecordDocumentParser):
    document_name = "Inventory"
    column_map = {
        'Description': 'description',
        'Quantity': 'qty',
        'Location': 'location',
        'Year Purchased': 'year_purchased',
        'Num of Years Remaining': 'years_remaining',
        'Cost when Purchased': 'net_purchase_cost',
        'Replacement Cost': 'net_replacement_cost',
        'Notes': 'notes'
    }


class RiskAssessmentParser(RecordDocumentParser):
    document_name = "Risk Assessment"
    column_map = {
        'Detail of hazard': 'hazard',
        'Who could be harmed by this hazard?': 'persons_at_risk',
        'Risk': 'risk',
        'Severity of hazard': 'severity',
        'If this hazard occurs, what will you do?': 'response',
        'What is currently done to avoid this hazard?': 'mitigation.current',
        'What more can be done to avoid this hazard?': 'mitigation.future.action',
        'Who will be responsible for doing this?': 'mitigation.future.person',
        'When will they do it by?': 'mitigation.future.deadline'
    }


class KeyListsParser(RecordDocumentParser):
    document_name = 'Key List'

    def list(self, club_id):
        enc_tab, document_soup = self.optimus_prime(club_id)

        out = {}

        # expand all the key lists
        key_list_tabs = enc_tab.find_all("tabenclosure")
        key_list_tab_ids = [unicode(x.attrs['id']) for x in key_list_tabs]

        for key_list_tab_id in key_list_tab_ids:
            # expand it
            self.eactivities.activate_tab(document_soup, key_list_tab_id)

            key_list_tab = document_soup.find("tabenclosure", id=key_list_tab_id)

            # process it
            item = self.handle_item(key_list_tab)
            out[item['id']] = item

        return out

    def item(self, club_id, id):
        enc_tab, document_soup = self.optimus_prime(club_id)
        key_list_tabs = enc_tab.find_all("tabenclosure")
        key_list_tab_ids = [unicode(x.attrs['id']) for x in key_list_tabs]

        for key_list_tab_id in key_list_tab_ids:
            # expand it
            self.eactivities.activate_tab(document_soup, key_list_tab_id)

            key_list_tab = document_soup.find("tabenclosure", id=key_list_tab_id)

            if unicode(id) not in key_list_tab.attrs['label']:
                continue

            # expand it
            self.eactivities.activate_tab(document_soup, key_list_tab_id)

            key_list_tab = document_soup.find("tabenclosure", id=key_list_tab_id)

            return self.handle_item(key_list_tab)
        return None

    def handle_item(self, key_list_tab):
        data = {}

        data['name'] = unicode(key_list_tab.attrs['label'])
        data['name'] = data['name'].replace('Key List ', '')
        data['id'], _, data['name'] = data['name'].partition(' - ')
        data['id'] = int(data['id'])
        data['people'] = []

        for record in key_list_tab.find_all("recordrow"):
            row_dict = {}

            person = record.find("field", attrs={'name': "Person"})
            name, cid = utils.split_role(unicode(person.attrs['value']))
            active = bool(record.find("field", attrs={'name': "Active"}).attrs['value'])

            row_dict['name'] = name
            row_dict['cid'] = cid
            row_dict['id'] = person.attrs['datum']
            row_dict['active'] = active

            data['people'].append(row_dict)

        return data
