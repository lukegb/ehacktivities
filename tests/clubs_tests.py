import unittest
import decimal

from mock import MagicMock
from bs4 import BeautifulSoup

from eactivities.models import Club
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

        self.club = Club(eactivities=self.eactivities, data={'id': 211})

    def boring_sideeffect(self, url):
        return (
            BeautifulSoup(
                self.response[url]
            ), None
        )

    def test_init(self):
        self.assertEquals(self.club.id, 211)

    def test_getattr(self):
        with self.assertRaises(AttributeError):
            self.club.lol
        self.assertEquals(self.club.name, "RCC FERRET FANCIERS")
        self.assertTrue(self.club.active)
        self.assertEquals(self.club.website, "http://www.union.ic.ac.uk/rcc/ffanciers")
        self.assertEquals(self.club.email, "ffanciers@imperial.ac.uk")
        self.assertEquals(self.club.current_profile_entry, {
            'short': u'A short description.',
            'long': u'A long description.'
        })
        self.assertEquals(self.club.membership.full_members, 342)
        self.assertEquals(self.club.membership.full_members_quota, 120)
        self.assertEquals(self.club.membership.membership_cost, decimal.Decimal('5.00'))
        self.assertEquals(self.club.membership.associate_members, 11)

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

        self.assertEquals(self.club.membership.full_members, 342)
        self.assertEquals(self.club.membership.full_members_quota, 120)
        self.assertEquals(self.club.membership.membership_cost, decimal.Decimal('5.00'))
        self.assertEquals(self.club.membership.associate_members, 11)
