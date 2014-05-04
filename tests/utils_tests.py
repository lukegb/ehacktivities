# vim: set fileencoding=utf-8

import unittest
import decimal

from eactivities import utils as utils


class TestFormatYear(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(utils.format_year(2013), "13-14")
        self.assertEqual(utils.format_year(2012), "12-13")
    
    def test_wraparound(self):
        self.assertEqual(utils.format_year(2000), "00-01")
        self.assertEqual(utils.format_year(1999), "99-00")
        

class TestSplitAccountBracket(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(
            utils.split_account_bracket("General (00)"),
            {'id': '00', 'name': 'General'}
        )
        self.assertEqual(
            utils.split_account_bracket("Event 1 (50)"),
            {'id': '50', 'name': 'Event 1'}
        )


class TestMungeValue(unittest.TestCase):
    def test_no_vat(self):
        self.assertEqual(
            utils.munge_value({
                'gross': 500
            }),
            {
                'gross': 500
            }
        )
        self.assertEqual(
            utils.munge_value({
                'net': 500
            }),
            {
                'net': 500
            }
        )
        self.assertEqual(
            utils.munge_value({
                'net': 500,
                'gross': 560
            }),
            {
                'net': 500,
                'gross': 560
            }
        )
        
    def test_vat_net_gross(self):
        self.assertEqual(
            utils.munge_value({
                'net': 500,
                'gross': 560,
                'vat': {
                    'rate': 'P1',
                    'value': decimal.Decimal(1.12)
                }
            }),
            {
                'net': 500,
                'gross': 560,
                'vat': {
                    'rate': 'P1',
                    'value': decimal.Decimal(1.12)
                }
            }
        )
        self.assertEqual(
            utils.munge_value({
                'net': 700,
                'gross': 560,
                'vat': {
                    'rate': 'P1',
                    'value': decimal.Decimal(1.12)
                }
            }),
            {
                'net': 700,
                'gross': 560,
                'vat': {
                    'rate': 'P1',
                    'value': decimal.Decimal(1.12)
                }
            }
        )
        
    def test_vat_net(self):
        self.assertEqual(
            utils.munge_value({
                'net': 500,
                'vat': {
                    'rate': 'P1',
                    'value': decimal.Decimal(1.2)
                }
            }),
            {
                'net': 500,
                'gross': 600,
                'vat': {
                    'rate': 'P1',
                    'value': decimal.Decimal(1.2)
                }
            }
        )
        self.assertEqual(
            utils.munge_value({
                'net': 500,
                'vat': {
                    'rate': 'P1',
                    'value': decimal.Decimal(1.175)
                }
            }),
            {
                'net': 500,
                'gross': 588,
                'vat': {
                    'rate': 'P1',
                    'value': decimal.Decimal(1.175)
                }
            }
        )
        
    def test_vat_gross(self):
        self.assertEqual(
            utils.munge_value({
                'gross': 600,
                'vat': {
                    'rate': 'P1',
                    'value': decimal.Decimal(1.2)
                }
            }),
            {
                'net': 500,
                'gross': 600,
                'vat': {
                    'rate': 'P1',
                    'value': decimal.Decimal(1.2)
                }
            }
        )
        self.assertEqual(
            utils.munge_value({
                'gross': 588,
                'vat': {
                    'rate': 'P1',
                    'value': decimal.Decimal(1.175)
                }
            }),
            {
                'net': 500,
                'gross': 588,
                'vat': {
                    'rate': 'P1',
                    'value': decimal.Decimal(1.175)
                }
            }
        )
        

class TestSplitRole(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(utils.split_role("A (BCD)"), ("A", "BCD"))
        self.assertEqual(utils.split_role("BCD (A)"), ("BCD", "A"))
        self.assertEqual(utils.split_role("A ((BCD))"), ("A", "(BCD)"))
        

class TestFormatPrice(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(utils.format_price('132.58'), 13258)
        self.assertEqual(utils.format_price('67'), 6700)
        self.assertEqual(utils.format_price('-79'), -7900)
        
    def test_extraneous_characters(self):
        self.assertEqual(utils.format_price(u'£24.33'), 2433)
        self.assertEqual(utils.format_price(u'£24.93p'), 2493)
        self.assertEqual(utils.format_price(u'-£14.33p'), -1433)
        
class TestQuantizeDecimal(unittest.TestCase):
    def test_simple(self):
        d = decimal.Decimal
        self.assertEqual(utils.quantize_decimal(d(143.2)), 143)
        self.assertEqual(utils.quantize_decimal(d(143.9)), 144)
        
        self.assertEqual(utils.quantize_decimal(d(144.2)), 144)
        self.assertEqual(utils.quantize_decimal(d(144.9)), 145)
        
    def test_rounding(self):
        d = decimal.Decimal
        self.assertEqual(utils.quantize_decimal(d(144.4)), 144)
        self.assertEqual(utils.quantize_decimal(d(144.5)), 145)
        self.assertEqual(utils.quantize_decimal(d(143.4)), 143)
        self.assertEqual(utils.quantize_decimal(d(143.5)), 144)
        