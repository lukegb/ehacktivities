import unittest
import decimal

from mock import MagicMock
from bs4 import BeautifulSoup

from eactivities import clubs
from . import xml


class TestClub(unittest.TestCase):
    def setUp(self):
        def invoke_sideeffect(*args):
            return self.boring_sideeffect(*args)

        self.eactivities = MagicMock()
        self.eactivities.load_and_start.side_effect = invoke_sideeffect

        self.response = {
            '/finance/transactions/211': xml.finance_transactions_211,
            '/admin/csp/details/211': xml.admin_csp_details_211,
        }

        self.club = clubs.Club(self.eactivities, 211)

    def boring_sideeffect(self, url):
        return (
            BeautifulSoup(
                self.response[url]
            ), None
        )

    def test_init(self):
        self.assertEquals(self.club.eactivities, self.eactivities)
        self.assertEquals(self.club.id, 211)
        self.assertEquals(self.club.name, "RCC FERRET FANCIERS")

    def test_getattr(self):
        self.eactivities.ajax_handler.return_value = BeautifulSoup(
            xml.admin_csp_details_211_tab395
        ), None
        with self.assertRaises(AttributeError):
            self.club.lol
        self.eactivities.ajax_handler.assert_called_with(
            {'navigate': '395', 'ajax': 'activatetabs'}
        )
        self.assertEquals(self.club.name, "RCC FERRET FANCIERS")
        self.assertTrue(self.club.active)
        self.assertEquals(self.club.website, "http://www.union.ic.ac.uk/rcc/ffanciers")
        self.assertEquals(self.club.email, "ffanciers@imperial.ac.uk")
        self.assertEquals(self.club.current_profile_entry, [
            u'A short description.',
            u'A long description.'
        ])
        self.assertEquals(self.club.members['full_members'], 342)
        self.assertEquals(self.club.members['full_members_quota'], 120)
        self.assertEquals(self.club.members['membership_cost'], decimal.Decimal('5.00'))
        self.assertEquals(self.club.members['associate_members'], 11)

    def test_getattr_noaccess(self):
        self.response['/admin/csp/details/211'] = xml.norecords
        with self.assertRaises(AttributeError):
            self.club.lol
        with self.assertRaises(AttributeError):
            self.club.website
        with self.assertRaises(AttributeError):
            self.club.email
        with self.assertRaises(AttributeError):
            self.club.active
        with self.assertRaises(AttributeError):
            self.club.current_profile_entry

        self.assertEquals(self.club.members['full_members'], 342)
        self.assertEquals(self.club.members['full_members_quota'], 120)
        self.assertEquals(self.club.members['membership_cost'], decimal.Decimal('5.00'))
        self.assertEquals(self.club.members['associate_members'], 11)
