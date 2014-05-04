import unittest
import decimal

from mock import MagicMock
from bs4 import BeautifulSoup

from eactivities import club_finances
from . import xml


class TestClubFinances(unittest.TestCase):
    def setUp(self):
        self.eactivities = MagicMock()
        self.club = MagicMock()
        self.club.eactivities = self.eactivities
        self.club.id = 211
        self.club_finances = club_finances.ClubFinances(self.club, 2013)

    def test_init(self):
        self.assertEquals(self.club_finances.club, self.club)
        self.assertEquals(self.club_finances.year, 2013)

    def test_getattr_this_year(self):
        self.assertFalse(self.club_finances.loaded_data)

        self.eactivities.load_and_start.return_value = BeautifulSoup(
            xml.finance_transactions_211
        ), None
        with self.assertRaises(AttributeError):
            self.club_finances.lol
        self.assertEquals(
            self.club_finances.funding_overview,
            {
                u'Harlington (2)': decimal.Decimal('0'),
                u'Grant (0)': decimal.Decimal('0'),
                u'SGI (1)': decimal.Decimal('1179.25')
            }
        )

        self.assertTrue(self.club_finances.loaded_data)

    def test_getattr_last_year(self):
        self.assertFalse(self.club_finances.loaded_data)

        def change_it(soup, tab_id):
            tab_soup = BeautifulSoup(xml.finance_transactions_211_2010)
            encid = tab_soup.data.encid.get_text()
            soup_enc = soup.find("enclosure", id=encid)
            soup_enc.clear()
            soup_enc.append(tab_soup.data)
            soup_enc.data.unwrap()

        self.club_finances.year = 2010
        self.eactivities.load_and_start.return_value = BeautifulSoup(
            xml.finance_transactions_211
        ), None
        self.eactivities.activate_tab.side_effect = change_it
        with self.assertRaises(AttributeError):
            self.club_finances.lol
        self.assertEquals(
            self.club_finances.funding_overview,
            {
                u'SGI (1)': decimal.Decimal('-1839.72')
            }
        )

        self.assertTrue(self.club_finances.loaded_data)