import decimal
import random
import os

import requests
from bs4 import BeautifulSoup

from . import exceptions, clubs

SESSION_COOKIE_NAME = 'ICU_eActivities'
BASE_PATH = 'https://eactivities.union.ic.ac.uk'
AJAX_HANDLER = BASE_PATH + '/common/ajax_handler.php'
FILE_HANDLER = BASE_PATH + '/common/file_handler.php'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 ' + \
             '(KHTML, like Gecko) Chrome/35.0.1916.86 Safari/537.36 ' + \
             'eHacktivities/1.0'

ESSL = os.getenv('EACTIVITIES_SSL_CERTIFICATE')


class EActivities(object):
    def __init__(self, session=None, credentials=None):
        self.session = requests.session()

        if ESSL:
            self.session.verify = ESSL

        self.session.headers.update({'User-Agent': USER_AGENT})

        if session is not None:
            # prime requests session
            self.session.get(BASE_PATH, cookies={SESSION_COOKIE_NAME, session})
        elif credentials is not None:
            # authenticate
            self.authenticate(credentials)

        self.load_roles()  # we need to do this on login, because eActivities

    def ajax_handler(self, data):
        try:
            resp = self.session.post(AJAX_HANDLER, data=data)
            resp.raise_for_status()
        except Exception as e:
            raise exceptions.EActivitiesServerException(e)

        soup = BeautifulSoup(resp.text)
        metadata = soup.metadata

        errorcode = int(metadata.errorcode.get_text())
        returncode = int(metadata.returnvalue.get_text())

        if errorcode == 0:  # all is well
            return soup, resp
        elif errorcode > 0:  # something went wrong
            raise exceptions.EActivitiesError(errorcode, returncode)
        elif errorcode == -1:
            # something is supposed to refresh?
            return soup, resp
        elif errorcode == -2:
            # "non-intrusive returns"
            return soup, resp
        elif errorcode == -3:
            # returns that "add value" but don't change data
            return soup, resp
        elif errorcode == -4:
            # reload the page
            return soup, resp
        elif errorcode == -5:
            # return to switchboard
            return soup, resp
        elif errorcode == -6:
            # confirmation
            return soup, resp
        else:
            raise exceptions.EActivitiesError(errorcode, returncode)

    def file_handler(self, file_id, override=False):
        return self.session.get(
            FILE_HANDLER,
            params={
                'rand': random.randint(100, 999),
                'rand2': random.randint(100, 999),
                'id': file_id,
                'override': 1 if override else 0
            },
            stream=True
        )

    def activate_tab(self, soup, tab_id):
        tab_soup, _ = self.ajax_handler({
            'ajax': 'activatetabs',
            'navigate': tab_id
        })
        encid = tab_soup.data.encid.get_text()
        soup_enc = soup.find("enclosure", id=encid)
        soup_enc.clear()
        soup_enc.append(tab_soup.data)
        soup_enc.data.unwrap()
        return soup

    def data_search(self, soup, tab_id, thing_id, tab=False):
        dssoup, _ = self.ajax_handler({
            'ajax': 'datasearch',
            'navigate': tab_id,
            'value': thing_id,
            'tab': tab
        })

        if dssoup.metadata.errorcode.get_text() == '-2' and \
                dssoup.metadata.returnvalue.get_text() == '0':
            return self.activate_tab(soup, tab_id)

        return soup

    def authenticate(self, credentials):
        soup, resp = self.ajax_handler({
            'ajax': 'login',
            'name': credentials[0],
            'pass': credentials[1],
            'objid': 1
        })

        if soup.metadata.returnvalue.get_text() != '1':
            raise exceptions.AuthenticationFailed("credentials invalid")

    def logout(self):
        self.ajax_handler({'ajax': 'logout', 'navigate': self.current_page_id})

    def load_and_start(self, url):
        try:
            resp = self.session.get(BASE_PATH + url)
            resp.raise_for_status()
        except Exception as e:
            raise exceptions.EActivitiesServerException(e)

        start_start = resp.text.find('start(')
        start_end = resp.text.find(',', start_start)
        page_id = int(resp.text[start_start+len('start('):start_end])

        self.current_page_id = page_id

        return self.ajax_handler({'ajax': 'setup', 'navigate': page_id})

    def get_inline_info(self):
        return self.ajax_handler({
            'ajax': 'setupinlineinfo',
            'navigate': self.current_page_id
        })

    def split_role(self, text):
        pos = len(text)
        cnt = 0
        for c in text[::-1]:
            pos -= 1
            if c == ')':
                cnt += 1
            elif c == '(':
                cnt -= 1
            if cnt == 0:
                return text[:pos-1], text[pos+1:-1]
            elif cnt < 0:
                raise ValueError("BRACKETS MISMATCH")
        raise ValueError("Couldn't find brackets enclosed value?!?")

    def format_price(self, text_price):
        price = ''.join([
            x for x in unicode(text_price) if x in '0123456789.-'
        ])
        dprice = decimal.Decimal(price)
        dprice *= 100
        return self.quantize_decimal(dprice)

    def quantize_decimal(self, dprice):
        return int(dprice.quantize(
            decimal.Decimal('1.'), rounding=decimal.ROUND_HALF_UP
        ))

    def load_roles(self):
        roles = {}
        self.load_and_start('/')

        # get the sidebar
        sidebar_soup, _ = self.get_inline_info()
        position, committee = self.split_role(
            sidebar_soup.find(class_="currentrole").get_text()
        )
        current_role = {
            'position': position,
            'committee': committee,
            'current': True
        }

        for role_option in sidebar_soup.data.find_all(
            'p', class_='otherroles'
        ):
            role_id = role_option.span.attrs['onclick']
            role_id = int(role_id[role_id.find("'")+1:role_id.rfind("'")])
            role_name = role_option.span.get_text()
            position, committee = self.split_role(role_name)
            roles[role_id] = {
                'id': role_id,
                'position': position,
                'committee': committee,
                'current': False
            }

        roles_soup, _ = self.ajax_handler({'ajax': 'roles', 'navigate': '1'})
        for role_menuopt in roles_soup.data.menu.find_all("menuopt"):
            role_id = role_menuopt.method.get_text()
            role_id = int(role_id[role_id.find("'")+1:role_id.rfind("'")])
            role_name = role_menuopt.label.get_text()
            position, committee = self.split_role(role_name)
            roles[role_id] = {
                'id': role_id,
                'position': position,
                'committee': committee,
                'current': False
            }

        # now try to work out what the current role is
        role_ids = set(roles.keys())
        max_role_id = max(roles.keys())
        for x in range(0, max_role_id):
            if x not in role_ids:
                current_role_id = x
                break
        else:
            current_role_id = max_role_id + 1

        current_role['id'] = current_role_id
        roles[current_role_id] = current_role

        self._roles = roles
        self.roles = lambda: self._roles

    def switch_role(self, role_id):
        self.ajax_handler({
            'ajax': 'changerole', 'navigate': '1', 'id': role_id
        })

        for _, role in self._roles.items():
            if role['current']:
                role['current'] = False
        self._roles[role_id]['current'] = True

    def club(self, club_id):
        return clubs.Club(self, club_id)

    def format_year(self, year):
        start_year = str(year % 100)[-2:]
        end_year = str((int(start_year) + 1) % 100)[-2:]
        return "{}-{}".format(start_year, end_year)

    def split_account_bracket(self, bracketed_text):
        thing_name, thing_id = self.split_role(bracketed_text)
        return {'id': thing_id, 'name': thing_name}

    def format_vat(self, vat_str):
        vat_type, vat_rate = self.split_role(vat_str)
        vat_type = vat_type[:vat_type.find(' ')]

        vat_rate = ''.join([
            x for x in unicode(vat_rate) if x in '0123456789.-'
        ])
        dvat_rate = decimal.Decimal(vat_rate)
        dvat_rate /= 100
        dvat_rate += 1

        return {'rate': vat_type, 'value': dvat_rate}

    def munge_value(self, value):
        if 'vat' not in value:
            return value

        if 'gross' in value and 'net' in value:
            return value
        elif 'gross' in value:
            dgross = decimal.Decimal(value['gross'])
            dnet = dgross / value['vat']['value']
            value['net'] = self.quantize_decimal(dnet)
        elif 'net' in value:
            dnet = decimal.Decimal(value['net'])
            dgross = dnet * value['vat']['value']
            value['gross'] = self.quantize_decimal(dgross)

        return value
