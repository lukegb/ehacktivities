import unittest
import decimal
import os
import datetime
import hashlib

from nose.plugins.attrib import attr

from eactivities import EActivities
from eactivities.parsers.documentation import InventoryParser, RiskAssessmentParser, KeyListsParser
import eactivities.parsers.finances as finance_parsers


# loading secrets from environment!
username = os.getenv('EHACK_TEST_USERNAME')
password = os.getenv('EHACK_TEST_PASSWORD')
test_club_id = int(os.getenv('EHACK_TEST_CLUB', '0'))

credentials = username is not None and password is not None and test_club_id


@attr('live')
class EActivitiesBaseTestCase(unittest.TestCase):
    _multiprocess_can_split_ = True

    def setUp(self):
        if not credentials:
            raise unittest.SkipTest("EHACK_TEST_* environment variables missing")

        self.eactivities = EActivities(credentials=(username, password.decode('base64')))

    def tearDown(self):
        self.eactivities.logout()


class RolesTestCase(EActivitiesBaseTestCase):
    def test_retrieve_role(self):
        roles = self.eactivities.roles()
        self.assertGreaterEqual(len(roles), 1)

        active_roles = sum([1 if x['current'] else 0 for x in roles.values()])
        self.assertEqual(active_roles, 1)

        for role_id, role in roles.items():
            self.assertEqual(role['id'], role_id)

    def test_change_role(self):
        roles = self.eactivities.roles()
        if len(roles) <= 1:
            raise unittest.SkipTest("need multiple roles to test switching")

        active_roles = [x for x in roles.values() if x['current']]
        inactive_roles = [x for x in roles.values() if not x['current']]
        self.assertEqual(len(active_roles), 1)
        self.assertGreaterEqual(len(inactive_roles), 1)

        old_role = active_roles[0]
        new_role = inactive_roles[0]

        self.eactivities.switch_role(new_role['id'])

        roles = self.eactivities.roles()

        active_roles = [x for x in roles.values() if x['current']]
        inactive_roles = [x for x in roles.values() if not x['current']]
        self.assertEqual(len(active_roles), 1)
        self.assertGreaterEqual(len(inactive_roles), 1)

        self.assertEqual(roles[old_role['id']]['current'], False)
        self.assertEqual(roles[new_role['id']]['current'], True)


class ClubBaseTestCase(EActivitiesBaseTestCase):
    def setUp(self):
        super(ClubBaseTestCase, self).setUp()

        self.club = self.eactivities.club(int(test_club_id))


class ClubTestCase(ClubBaseTestCase):
    def test_visible(self):
        self.assertTrue(self.club.active)
        self.assertIsNotNone(self.club.website)
        self.assertIsNotNone(self.club.email)
        self.assertIsNotNone(self.club.current_profile_entry)
        self.assertEqual(len(self.club.current_profile_entry), 2)
        self.assertIsNotNone(self.club.membership)
        self.assertIsNotNone(self.club.membership.full_members)
        self.assertIsNotNone(self.club.membership.full_members_quota)
        self.assertIsNotNone(self.club.membership.associate_members)
        self.assertIsNotNone(self.club.membership.membership_cost)

    def test_not_visible(self):
        self.club = self.eactivities.club(406)  # just hope leosoc never use this
        with self.assertRaises(AttributeError):
            self.club.active
        with self.assertRaises(AttributeError):
            self.club.email
        with self.assertRaises(AttributeError):
            self.club.current_profile_entry
        self.assertIsNotNone(self.club.membership)
        self.assertIsNotNone(self.club.membership.full_members)
        self.assertIsNotNone(self.club.membership.full_members_quota)
        self.assertIsNotNone(self.club.membership.associate_members)
        self.assertIsNotNone(self.club.membership.membership_cost)


class ClubDocumentationTestCase(ClubBaseTestCase):
    def setUp(self):
        super(ClubDocumentationTestCase, self).setUp()

    def test_inventory(self):
        inv_list = InventoryParser(self.eactivities).fetch_data(test_club_id)

        if inv_list is None:
            raise unittest.SkipTest("Inventory exempt - can't test parsing")

        self.assertGreater(len(inv_list), 0)
        self.assertItemsEqual(inv_list[0].keys(), [
            'id',
            'description',
            'qty',
            'location',
            'year_purchased',
            'years_remaining',
            'net_purchase_cost',
            'net_replacement_cost',
            'notes'
        ])

    def test_risk_assessment(self):
        ra_list = RiskAssessmentParser(self.eactivities).fetch_data(test_club_id)

        if ra_list is None:
            raise unittest.SkipTest("Risk Assessment exempt - can't test parsing")

        self.assertGreater(len(ra_list), 0)
        self.assertItemsEqual(ra_list[0].keys(), [
            'id',
            'hazard',
            'persons_at_risk',
            'risk',
            'severity',
            'response',
            'mitigation'
        ])
        self.assertIn('mitigation', ra_list[0])
        self.assertIn('current', ra_list[0]['mitigation'])
        self.assertIn('future', ra_list[0]['mitigation'])
        self.assertIn('action', ra_list[0]['mitigation']['future'])
        self.assertIn('person', ra_list[0]['mitigation']['future'])
        self.assertIn('deadline', ra_list[0]['mitigation']['future'])

    def test_key_lists(self):
        klp = KeyListsParser(self.eactivities)
        kls = klp.fetch_data(test_club_id)

        for key_list in kls.values():
            self.assertIn('id', key_list)

            key_list_item = klp.item(test_club_id, key_list['id'])
            self.assertEqual(key_list_item, key_list)

            self.assertItemsEqual(key_list_item.keys(), [
                'id', 'name', 'people'
            ])
            for person in key_list_item['people']:
                self.assertItemsEqual(person.keys(), [
                    'name', 'cid', 'id', 'active'
                ])


class ClubFinanceTestCase(ClubBaseTestCase):
    def setUp(self):
        super(ClubFinanceTestCase, self).setUp()

        self.f = self.club.finances(2012)
        self.year = 2012

    def test_overview(self):
        fo = self.f.funding_overview
        self.assertGreater(len(fo), 1)

    def test_banking_records(self):
        br = finance_parsers.BankingRecordsParser(self.eactivities)
        brl = br.list(test_club_id, self.year)

        if len(brl) > 0:
            brl_zero = brl[0]
            brl_zero_item = br.item(test_club_id, self.year, brl_zero['id'])
            self.assertEqual(brl_zero['id'], brl_zero_item['id'])
            self.assertEqual(brl_zero['gross_amount'], brl_zero_item['gross_amount'])

            self.assertItemsEqual(brl_zero.keys(), [
                'id', 'gross_amount'
            ])
            self.assertItemsEqual(brl_zero_item.keys(), [
                'id', 'date', 'transaction_lines', 'gross_amount',
                'paying_in_slips'
            ])
            self.assertEqual(len(brl_zero_item['paying_in_slips']), 1)

            br.pdf(club_id=test_club_id, year=self.year, item_id=brl_zero_item['id'], image_id=brl_zero_item['paying_in_slips'][0])

    def test_sales_invoices(self):
        si = finance_parsers.SalesInvoicesParser(self.eactivities)
        sil = si.list(test_club_id, self.year)

        if len(sil) > 0:
            sil_zero = sil[0]
            sil_zero_item = si.item(test_club_id, self.year, sil_zero['id'])
            self.assertEqual(sil_zero['id'], sil_zero_item['id'])
            self.assertEqual(sil_zero['date'], sil_zero_item['date'])
            self.assertEqual(sil_zero['customer']['name'], sil_zero_item['customer']['name'])
            self.assertEqual(sil_zero['customer_purchase_order_number'], sil_zero_item['customer_purchase_order_number'])
            self.assertEqual(sil_zero['gross_amount'], sil_zero_item['gross_amount'])

            self.assertItemsEqual(sil_zero.keys(), [
                'id', 'date', 'customer',
                'customer_purchase_order_number', 'gross_amount',
                'status'
            ])
            self.assertItemsEqual(sil_zero_item.keys(), [
                'id', 'date', 'customer', 'international',
                'customer_purchase_order_number', 'audit_trail',
                'next_authorisers', 'transaction_lines',
                'gross_amount', 'purchase_order_attachments',
                'status'
            ])

            si.item_pdf(sil_zero_item['id'])

            if len(sil_zero_item['purchase_order_attachments']) > 1:
                si.pdf(
                    club_id=test_club_id,
                    year=self.year,
                    item_id=sil_zero_item['id'],
                    image_id=sil_zero_item['purchase_order_attachments'][0]
                )

    def test_claims(self):
        cl = finance_parsers.ClaimsParser(self.eactivities)
        cll = cl.list(test_club_id, self.year)

        if len(cll) > 0:
            cll_zero = cll[0]
            cll_zero_item = cl.item(test_club_id, self.year, cll_zero['id'])
            self.assertEqual(cll_zero['id'], cll_zero_item['id'])
            self.assertEqual(cll_zero['person'], cll_zero_item['person'])
            self.assertEqual(cll_zero['status'], cll_zero_item['status'])
            self.assertEqual(cll_zero['payment_date'], cll_zero_item['payment_date'])
            self.assertEqual(cll_zero['gross_amount'], cll_zero_item['gross_amount'])

            self.assertItemsEqual(cll_zero.keys(), [
                'id', 'person', 'status', 'payment_date', 'gross_amount'
            ])
            self.assertItemsEqual(cll_zero_item.keys(), [
                'id', 'payment_date', 'person', 'notes', 'gross_amount',
                'status', 'audit_trail', 'next_authorisers', 'transaction_lines',
                'receipts'
            ])

            if len(cll_zero_item['receipts']) > 1:
                cl.pdf(club_id=test_club_id, year=self.year, item_id=cll_zero_item['id'], image_id=cll_zero_item['receipts'][0])

    def test_purchase_orders(self):
        po = finance_parsers.PurchaseOrdersParser(self.eactivities)
        pol = po.list(test_club_id, self.year)

        if len(pol) > 0:
            pol_zero = pol[0]
            pol_zero_item = po.item(test_club_id, self.year, pol_zero['id'])
            self.assertEqual(pol_zero['id'], pol_zero_item['id'])
            self.assertEqual(pol_zero['supplier']['name'], pol_zero['supplier']['name'])
            self.assertEqual(pol_zero['status'], pol_zero_item['status'])
            self.assertEqual(pol_zero['payment_date'], pol_zero_item['payment_date'])
            self.assertEqual(pol_zero['gross_amount'], pol_zero_item['gross_amount'])
            self.assertEqual(pol_zero['invoice_received'], pol_zero_item['invoice_received'])
            self.assertEqual(pol_zero['finished_goods_receipting'], pol_zero_item['finished_goods_receipting'])
            self.assertEqual(pol_zero['pro_forma'], pol_zero_item['pro_forma'])

            self.assertItemsEqual(pol_zero.keys(), [
                'id', 'supplier', 'status', 'payment_date', 'gross_amount', 'invoice_received', 'finished_goods_receipting',
                'pro_forma'
            ])
            self.assertItemsEqual(pol_zero_item.keys(), [
                'id', 'payment_date', 'supplier', 'status', 'audit_trail', 'next_authorisers',
                'transaction_lines', 'invoice_received', 'finished_goods_receipting', 'pro_forma',
                'gross_amount', 'invoices'
            ])

            if len(pol_zero_item['invoices']) > 1:
                po.pdf(club_id=test_club_id, year=self.year, item_id=pol_zero_item['id'], image_id=pol_zero_item['invoices'][0])

    def test_transaction_corrections(self):
        tc = finance_parsers.TransactionCorrectionsParser(self.eactivities)
        tcl = tc.list(test_club_id, self.year)

        if len(tcl) > 0:
            tcl_zero = tcl[0]
            tcl_zero_item = tc.item(test_club_id, self.year, tcl_zero['id'])
            self.assertEqual(tcl_zero['id'], tcl_zero_item['id'])
            self.assertEqual(tcl_zero['status'], tcl_zero_item['status'])
            self.assertEqual(tcl_zero['gross_amount'], tcl_zero_item['gross_amount'])

            self.assertItemsEqual(tcl_zero.keys(), [
                'id', 'status', 'gross_amount'
            ])
            self.assertItemsEqual(tcl_zero_item.keys(), [
                'id', 'gross_amount', 'status', 'audit_trail', 'next_authorisers',
                'from_transaction_lines', 'to_transaction_lines'
            ])

    def test_internal_charges(self):
        ic = finance_parsers.InternalChargesParser(self.eactivities)
        icl = ic.list(test_club_id, self.year)

        if len(icl) > 0:
            icl_zero = icl[0]
            icl_zero_item = ic.item(test_club_id, self.year, icl_zero['id'])
            self.assertEqual(icl_zero['id'], icl_zero_item['id'])
            self.assertEqual(icl_zero['status'], icl_zero_item['status'])
            self.assertEqual(icl_zero['gross_amount'], icl_zero_item['gross_amount'])
            self.assertEqual(icl_zero['charged_committee'], icl_zero_item['charged_committee'])
            self.assertEqual(icl_zero['receiving_committee'], icl_zero_item['receiving_committee'])

            self.assertItemsEqual(icl_zero.keys(), [
                'id', 'status', 'gross_amount', 'charged_committee', 'receiving_committee'
            ])
            self.assertItemsEqual(icl_zero_item.keys(), [
                'id', 'status', 'gross_amount', 'charged_committee', 'receiving_committee',
                'notes', 'audit_trail', 'next_authorisers', 'transaction_lines'
            ])

    def test_members_funds_redistributions(self):
        mfr = finance_parsers.MembersFundsRedistributionsParser(self.eactivities)
        mfrl = mfr.list(test_club_id, self.year)

        if len(mfrl) > 0:
            mfrl_zero = mfrl[0]
            mfrl_zero_item = mfr.item(test_club_id, self.year, mfrl_zero['id'])
            self.assertEqual(mfrl_zero['id'], mfrl_zero_item['id'])
            self.assertEqual(mfrl_zero['person'], mfrl_zero_item['person'])
            self.assertEqual(mfrl_zero['status'], mfrl_zero_item['status'])
            self.assertEqual(mfrl_zero['funding_source'], mfrl_zero_item['funding_source'])
            self.assertEqual(mfrl_zero['gross_amount'], mfrl_zero_item['gross_amount'])

            self.assertItemsEqual(mfrl_zero.keys(), [
                'id', 'person', 'status', 'funding_source', 'gross_amount'
            ])
            self.assertItemsEqual(mfrl_zero_item.keys(), [
                'id', 'person', 'funding_source', 'gross_amount', 'notes',
                'status', 'audit_trail', 'next_authorisers', 'from_transaction_lines',
                'to_transaction_lines'
            ])

    def test_funding_redistributions(self):
        fr = finance_parsers.FundingRedistributionsParser(self.eactivities)
        frl = fr.list(test_club_id, self.year)

        if len(frl) > 0:
            frl_zero = frl[0]
            frl_zero_item = fr.item(test_club_id, self.year, frl_zero['id'])
            self.assertEqual(frl_zero['id'], frl_zero_item['id'])
            self.assertEqual(frl_zero['status'], frl_zero_item['status'])
            self.assertEqual(frl_zero['funding_source'], frl_zero_item['funding_source'])
            self.assertEqual(frl_zero['gross_amount'], frl_zero_item['gross_amount'])

            self.assertItemsEqual(frl_zero.keys(), [
                'id', 'status', 'funding_source', 'gross_amount'
            ])
            self.assertItemsEqual(frl_zero_item.keys(), [
                'id', 'funding_source', 'gross_amount',
                'status', 'audit_trail', 'next_authorisers', 'from_transaction_lines',
                'to_transaction_lines'
            ])


class ClubFinanceCinemaTestCase(ClubBaseTestCase):
    def setUp(self):
        super(ClubFinanceCinemaTestCase, self).setUp()

        if test_club_id != 411:
            raise unittest.SkipTest("results stored only for 411")

        self.year = 2012
        self.f = self.club.finances(self.year)

    def fetch_sha1(self, thing):
        s = hashlib.sha1()
        for chunk in thing.iter_content(1024):
            s.update(chunk)
        return s.hexdigest()

    def hash_sha1(self, thing):
        s = hashlib.sha1()
        s.update(unicode(thing))
        return s.hexdigest()

    # def print_val(self, x, y):
    #     print 'Wanted', x, '==', y

    def test_overview(self):
        fo = self.f.funding_overview
        self.assertEqual(len(fo), 3)
        self.assertEqual(fo['Grant (0)'], decimal.Decimal('0'))
        self.assertEqual(fo['SGI (1)'], decimal.Decimal('-3964.64'))
        self.assertEqual(fo['Harlington (2)'], decimal.Decimal('-13095.89'))

    def test_banking_records(self):
        br = finance_parsers.BankingRecordsParser(self.eactivities)
        brl = br.list(test_club_id, self.year)
        self.assertEqual(len(brl), 11)
        self.assertItemsEqual([x['id'] for x in brl], [
            u'124830', u'124831', u'124832', u'124833', u'124834', u'124835', u'124836',
            u'141013', u'141014', u'141015', u'141016'
        ])
        br_x = [x['gross_amount'] for x in brl if x['id'] == u'124830'][0]
        self.assertEqual(br_x, decimal.Decimal('606.33'))

        bri = br.item(test_club_id, self.year, u'124830')
        self.assertEqual(bri['date'], datetime.date(2012, 10, 16))
        self.assertEqual(len(bri['transaction_lines']), 5)
        self.assertEqual(
            self.fetch_sha1(br.pdf(club_id=test_club_id, year=self.year, item_id=bri['id'], image_id=bri['paying_in_slips'][0])),
            'a5ba9d8b9efca6f593d7af5046c9fe7de32c7b09'
        )

    def test_sales_invoices(self):
        si = finance_parsers.SalesInvoicesParser(self.eactivities)
        sil = si.list(test_club_id, self.year)
        self.assertEqual(len(sil), 1)
        self.assertItemsEqual([x['id'] for x in sil], [u'602067'])

        sil_item = sil[0]
        self.assertEqual(sil_item['id'], u'602067')
        self.assertEqual(sil_item['date'], datetime.date(2013, 6, 25))
        self.assertEqual(self.hash_sha1(sil_item['customer']['name']), 'a3ae5fd8f109c048aacd30440dbf218fde69d936')
        self.assertIsNone(sil_item['customer_purchase_order_number'])
        self.assertEqual(sil_item['gross_amount'], decimal.Decimal('334.72'))
        self.assertEqual(sil_item['status'], 'COMPLETED')

        sii = si.item(test_club_id, self.year, u'602067')
        self.assertEqual(sii['id'], sil_item['id'])
        self.assertEqual(sii['date'], sil_item['date'])
        self.assertEqual(sii['customer']['name'], sil_item['customer']['name'])
        self.assertEqual(sii['customer_purchase_order_number'], sil_item['customer_purchase_order_number'])
        self.assertEqual(sii['gross_amount'], sil_item['gross_amount'])
        self.assertEqual(sii['status'], sil_item['status'])

        self.assertEqual(self.hash_sha1(sii['customer']['address']), '124418ea0fb98bbee68e4a8124954ca564716d7f')
        self.assertEqual(self.hash_sha1(sii['customer']['contact']['name']), '3333834532534d99a8a54b04f210211262f9b90b')
        self.assertEqual(self.hash_sha1(sii['customer']['contact']['phone']), 'ac653ab83d1553d0a28dac8b20aac29eb2e7b227')
        self.assertEqual(self.hash_sha1(sii['customer']['contact']['email']), '26cc3807a049785ba8d286b2834e29bfb450f574')
        self.assertFalse(sii['international'])

        self.assertEqual(len(sii['audit_trail']), 2)
        hashed_at = [dict([(a, self.hash_sha1(unicode(b))) for (a, b) in line.items()]) for line in sii['audit_trail']]
        self.assertEqual(hashed_at[0]['role'], '70f7b048909aab7189f17304a27c8a23618d772b')
        self.assertEqual(hashed_at[0]['name'], 'fe415757c4183ce3edcac2b560cabcc755b71068')
        self.assertEqual(hashed_at[0]['notes'], '59485474e0259a370fa35b4cbf7b12da5791a4d1')
        self.assertEqual(hashed_at[0]['date'], '40ea7fae3fda0a8cb546490dbe96f027e2b3ce8b')

        self.assertEqual(hashed_at[1]['role'], '862826083e8399c6709108c51688ef53ee0b6218')
        self.assertEqual(hashed_at[1]['name'], '6178539ac523e4e9c9bd4ba68906c30c611ab356')
        self.assertEqual(hashed_at[1]['notes'], 'b917a98575e20887318e613d130b74b32ad5f506')
        self.assertEqual(hashed_at[1]['date'], '55e71acc312e6e2ec0167b04aa6f43871d3d9c04')

        self.assertEqual(len(sii['transaction_lines']), 1)
        self.assertEqual(sii['transaction_lines'][0]['description'], 'BBC Bits and Bobs (Left Over)')
        self.assertEqual(sii['transaction_lines'][0]['account'], {'id': '450', 'name': 'Goods & Services'})
        self.assertEqual(sii['transaction_lines'][0]['activity'], {'id': '58', 'name': 'Equipment Renewal Fund Raising'})
        self.assertEqual(sii['transaction_lines'][0]['funding_source'], {'id': '1', 'name': 'SGI'})
        self.assertEqual(sii['transaction_lines'][0]['value']['vat'], {'rate': 'S1', 'value': decimal.Decimal('1.2')})
        self.assertEqual(sii['transaction_lines'][0]['value']['gross'], decimal.Decimal('334.72'))
        self.assertEqual(sii['transaction_lines'][0]['unit_value']['vat'], {'rate': 'S1', 'value': decimal.Decimal('1.2')})
        self.assertEqual(sii['transaction_lines'][0]['unit_value']['gross'], decimal.Decimal('334.72'))
        self.assertEqual(sii['transaction_lines'][0]['quantity'], 1)

        self.assertEqual(
            self.fetch_sha1(si.pdf(club_id=test_club_id, year=self.year, item_id=sii['id'], image_id=sii['purchase_order_attachments'][0])),
            'cc9ccb9807694f654aed6ddd590ac404d40ca3e0'
        )

    def test_claims(self):
        cl = finance_parsers.ClaimsParser(self.eactivities)
        cll = cl.list(test_club_id, self.year)
        self.assertEqual(len(cll), 74)
        self.assertItemsEqual([x['id'] for x in cll], [
            u'5854', u'5884', u'5885', u'5886', u'5942',
            u'5945', u'5946', u'5948', u'5949', u'5950',
            u'6036', u'6070', u'6114', u'6135', u'6158',
            u'6305', u'6434', u'6476', u'6477', u'6479',
            u'6517', u'6569', u'6642', u'6643', u'6747',
            u'6945', u'7178', u'7393', u'7499', u'7653',
            u'7654', u'7655', u'7656', u'7657', u'7658',
            u'7659', u'7660', u'7734', u'7981', u'7982',
            u'8001', u'8003', u'8004', u'8005', u'8006',
            u'8295', u'8391', u'8424', u'8425', u'8427',
            u'8428', u'8429', u'8430', u'8431', u'8434',
            u'8435', u'8596', u'8651', u'9249', u'9260',
            u'9261', u'9262', u'9263', u'9285', u'9349',
            u'9562', u'10230', u'10315', u'10385', u'10390',
            u'10392', u'10394', u'10405', u'10420'
        ])
        cll_item = cll[0]
        self.assertEqual(cll_item['id'], u'5854')
        self.assertEqual(self.hash_sha1(cll_item['person']), '0fc809085b837fa907456c23b6c57bcfe4086573')
        self.assertEqual(cll_item['status'], 'COMPLETED')
        self.assertEqual(cll_item['payment_date'], datetime.date(2012, 10, 18))
        self.assertEqual(cll_item['gross_amount'], decimal.Decimal('6.75'))

        cli = cl.item(test_club_id, self.year, u'5854')
        self.assertEqual(cll_item['id'], cli['id'])
        self.assertEqual(self.hash_sha1(cll_item['person']), self.hash_sha1(cli['person']))
        self.assertEqual(cll_item['status'], cli['status'])
        self.assertEqual(cll_item['payment_date'], cli['payment_date'])
        self.assertEqual(cll_item['gross_amount'], cli['gross_amount'])

        self.assertEqual(self.hash_sha1(cli['notes']), '3259df291476f350af83d00370cf81f8ba98b5b6')
        self.assertEqual(len(cli['transaction_lines']), 1)
        self.assertEqual(cli['transaction_lines'][0]['description'], 'GSA Pizza Collection')
        self.assertEqual(cli['transaction_lines'][0]['account'], {'id': '630', 'name': 'Carriage'})
        self.assertEqual(cli['transaction_lines'][0]['activity'], {'id': '57', 'name': 'Cinema Hire'})
        self.assertEqual(cli['transaction_lines'][0]['funding_source'], {'id': '1', 'name': 'SGI'})
        self.assertEqual(cli['transaction_lines'][0]['consolidation'], {'id': '0', 'name': 'External'})
        self.assertEqual(cli['transaction_lines'][0]['value']['vat'], {'rate': 'P1', 'value': decimal.Decimal('1.2')})
        self.assertEqual(cli['transaction_lines'][0]['value']['gross'], decimal.Decimal('6.75'))

        hashed_at = [dict([(a, self.hash_sha1(unicode(b))) for (a, b) in line.items()]) for line in cli['audit_trail']]
        self.assertEqual(hashed_at[0]['role'], 'fbf371a6a4938e4abcd1702439c70246b407057c')
        self.assertEqual(hashed_at[0]['name'], '0fc809085b837fa907456c23b6c57bcfe4086573')
        self.assertEqual(hashed_at[0]['notes'], 'ed2234b81e1992648dc8e50566bd81e00b87886d')
        self.assertEqual(hashed_at[0]['date'], 'dc94adee62044d2bf6587c1dde8dec80d0c73e4c')

        self.assertEqual(hashed_at[1]['role'], '70f7b048909aab7189f17304a27c8a23618d772b')
        self.assertEqual(hashed_at[1]['name'], 'fe415757c4183ce3edcac2b560cabcc755b71068')
        self.assertEqual(hashed_at[1]['notes'], '4b8383d6bc4543fec7d27c04c57f05054bb06252')
        self.assertEqual(hashed_at[1]['date'], '26a07a91710859901091512650b1542cda30f7e3')

        self.assertEqual(
            self.fetch_sha1(cl.pdf(club_id=test_club_id, year=self.year, item_id=cli['id'], image_id=cli['receipts'][0])),
            '9258149cef4416566134a84fcdbf638e977a4e48'
        )

    def test_purchase_orders(self):
        po = finance_parsers.PurchaseOrdersParser(self.eactivities)
        pol = po.list(test_club_id, self.year)
        self.assertEqual(len(pol), 62)
        self.assertItemsEqual([x['id'] for x in pol], [
            u"5002057", u"5002072", u"5002129", u"5002388", u"5002389",
            u"5002486", u"5002620", u"5002621", u"5002622", u"5002623",
            u"5002640", u"5002643", u"5002699", u"5002800", u"5002902",
            u"5002990", u"5002991", u"5002992", u"5002993", u"5002994",
            u"5002995", u"5002996", u"5002997", u"5003063", u"5003064",
            u"5003139", u"5003176", u"5003267", u"5003310", u"5003312",
            u"5003315", u"5003316", u"5003317", u"5003318", u"5003319",
            u"5003347", u"5003391", u"5003400", u"5003488", u"5003500",
            u"5003668", u"5003669", u"5003670", u"5003671", u"5003672",
            u"5003673", u"5003690", u"5003691", u"5003754", u"5003807",
            u"5003875", u"5004043", u"5004058", u"5004081", u"5004143",
            u"5004147", u"5004150", u"5004151", u"5004173", u"5004226",
            u"5004232", u"5004265",
        ])

        pol_item = pol[0]
        self.assertEqual(pol_item['id'], u'5002057')
        self.assertEqual(self.hash_sha1(pol_item['supplier']['name']), 'a93d63b170729bc391cf37a9ae78ab07dd1ef22a')
        self.assertEqual(pol_item['status'], 'COMPLETED')
        self.assertTrue(pol_item['invoice_received'])
        self.assertTrue(pol_item['finished_goods_receipting'])
        self.assertFalse(pol_item['pro_forma'])
        self.assertEqual(pol_item['payment_date'], datetime.date(2012, 10, 2))
        self.assertEqual(pol_item['gross_amount'], decimal.Decimal('120.00'))

        poi = po.item(test_club_id, self.year, u'5002057')
        self.assertEqual(poi['id'], u'5002057')
        self.assertEqual(poi['supplier']['name'], pol_item['supplier']['name'])
        self.assertEqual(self.hash_sha1(poi['supplier']['address']), 'e3b54db257c9fc535a312bac319b1ae83c04e1b2')
        self.assertEqual(poi['status'], pol_item['status'])
        self.assertEqual(poi['invoice_received'], pol_item['invoice_received'])
        self.assertEqual(poi['finished_goods_receipting'], pol_item['finished_goods_receipting'])
        self.assertEqual(poi['pro_forma'], pol_item['pro_forma'])

        hashed_at = [dict([(a, self.hash_sha1(unicode(b))) for (a, b) in line.items()]) for line in poi['audit_trail']]
        self.assertEqual(hashed_at[0]['role'], 'e65ba88cb325cece120babdb95d28f0b1e1db9f5')
        self.assertEqual(hashed_at[0]['name'], 'fe415757c4183ce3edcac2b560cabcc755b71068')
        self.assertEqual(hashed_at[0]['notes'], '303b0d773f8e099e0d84586784d2ba547d05a792')
        self.assertEqual(hashed_at[0]['date'], 'ef6cbbb3b36cbb765b2a2cc6a56f6fcd6745b6e8')

        self.assertEqual(hashed_at[1]['role'], '55cf5ee221a461c8b3db07cb613622ac61403013')
        self.assertEqual(hashed_at[1]['name'], '33c3bf7adc0ec7a2cbc15e54dc7f138bc90aac14')
        self.assertEqual(hashed_at[1]['notes'], '5987c7f90f0229c88d4d66b1ca0107097176987e')
        self.assertEqual(hashed_at[1]['date'], 'ef6cbbb3b36cbb765b2a2cc6a56f6fcd6745b6e8')

        self.assertEqual(hashed_at[2]['role'], 'e2cf8b0754d2be61073416142f53a7cde5669bfc')
        self.assertEqual(hashed_at[2]['name'], 'e77601345ce74019c1f504b4732e973645a2ed08')
        self.assertEqual(hashed_at[2]['notes'], '383cc071f1c2da4dc003a2fb3bca6749b3fe7c60')
        self.assertEqual(hashed_at[2]['date'], 'ef6cbbb3b36cbb765b2a2cc6a56f6fcd6745b6e8')

        self.assertEqual(len(poi['transaction_lines']), 1)
        self.assertEqual(poi['transaction_lines'][0]['description'], 'Sherlock Holmes II')
        self.assertEqual(poi['transaction_lines'][0]['account'], {'id': '725', 'name': 'Copyright & Royalties'})
        self.assertEqual(poi['transaction_lines'][0]['activity'], {'id': '53', 'name': 'Spring All-Nighter'})
        self.assertEqual(poi['transaction_lines'][0]['funding_source'], {'id': '1', 'name': 'SGI'})
        self.assertEqual(poi['transaction_lines'][0]['consolidation'], {'id': '0', 'name': 'External'})
        self.assertEqual(poi['transaction_lines'][0]['value']['vat'], {'rate': 'P1', 'value': decimal.Decimal('1.2')})
        self.assertEqual(poi['transaction_lines'][0]['value']['gross'], decimal.Decimal('120.00'))
        self.assertEqual(poi['transaction_lines'][0]['unit_value']['vat'], {'rate': 'P1', 'value': decimal.Decimal('1.2')})
        self.assertEqual(poi['transaction_lines'][0]['unit_value']['gross'], decimal.Decimal('120.00'))
        self.assertEqual(poi['transaction_lines'][0]['quantity']['received'], 1.0)
        self.assertEqual(poi['transaction_lines'][0]['quantity']['ordered'], 1.0)

    def test_transaction_corrections(self):
        tc = finance_parsers.TransactionCorrectionsParser(self.eactivities)
        tcl = tc.list(test_club_id, self.year)

        self.assertEqual(len(tcl), 10)
        self.assertItemsEqual([x['id'] for x in tcl], [
            u'371', u'378', u'403', u'482', u'530',
            u'576', u'582', u'647', u'909', u'943'
        ])

        tcl_item = tcl[0]
        self.assertEqual(tcl_item['id'], u'371')
        self.assertEqual(tcl_item['status'], u'COMPLETED')
        self.assertEqual(tcl_item['gross_amount'], decimal.Decimal('495.33'))

        tci = tc.item(test_club_id, self.year, tcl_item['id'])
        self.assertEqual(tci['id'], tcl_item['id'])
        self.assertEqual(tci['status'], tcl_item['status'])
        self.assertEqual(tci['gross_amount'], tcl_item['gross_amount'])

        self.assertEqual(len(tci['from_transaction_lines']), 3)
        x = [
            {
                'description': u'Exhaust Grant',
                'account': {'id': u'640', 'name': u'Consumables'},
                'activity': {'id': u'00', 'name': u'General'},
                'funding_source': {'id': u'0', 'name': u'Grant'},
                'value': {'gross': decimal.Decimal('50.00')},
            },
            {
                'description': u'Exhaust Grant',
                'account': {'id': u'685', 'name': u'Equipment Purchase'},
                'activity': {'id': u'00', 'name': u'General'},
                'funding_source': {'id': u'0', 'name': u'Grant'},
                'value': {'gross': decimal.Decimal('200.00')},
            },
            {
                'description': u'Exhaust Grant',
                'account': {'id': u'725', 'name': u'Copyright & Royalties'},
                'activity': {'id': u'00', 'name': u'General'},
                'funding_source': {'id': u'0', 'name': u'Grant'},
                'value': {'gross': decimal.Decimal('245.33')},
            },
        ]
        self.assertEqual(tci['from_transaction_lines'], x)

        self.assertEqual(len(tci['to_transaction_lines']), 3)
        x = [
            {
                'description': u'Exhaust Grant',
                'account': {'id': u'640', 'name': u'Consumables'},
                'activity': {'id': u'00', 'name': u'General'},
                'funding_source': {'id': u'1', 'name': u'SGI'},
                'value': {'gross': decimal.Decimal('50.00')},
            },
            {
                'description': u'Exhaust Grant',
                'account': {'id': u'685', 'name': u'Equipment Purchase'},
                'activity': {'id': u'00', 'name': u'General'},
                'funding_source': {'id': u'1', 'name': u'SGI'},
                'value': {'gross': decimal.Decimal('200.00')},
            },
            {
                'description': u'Exhaust Grant',
                'account': {'id': u'725', 'name': u'Copyright & Royalties'},
                'activity': {'id': u'00', 'name': u'General'},
                'funding_source': {'id': u'1', 'name': u'SGI'},
                'value': {'gross': decimal.Decimal('245.33')},
            },
        ]
        self.assertEqual(tci['to_transaction_lines'], x)

        self.assertEqual(len(tci['audit_trail']), 2)
        self.assertEqual(self.hash_sha1(tci['audit_trail'][0]['role']), '70f7b048909aab7189f17304a27c8a23618d772b')
        self.assertEqual(self.hash_sha1(tci['audit_trail'][0]['name']), 'fe415757c4183ce3edcac2b560cabcc755b71068')
        self.assertEqual(self.hash_sha1(tci['audit_trail'][0]['notes']), '65bd5f5a07b1bc471591620888b5beec6ae47b80')
        self.assertEqual(self.hash_sha1(tci['audit_trail'][0]['date']), '59f8d084dc869f265a4910748c7115989312dce3')

        self.assertEqual(self.hash_sha1(tci['audit_trail'][1]['role']), 'e2cf8b0754d2be61073416142f53a7cde5669bfc')
        self.assertEqual(self.hash_sha1(tci['audit_trail'][1]['name']), 'e77601345ce74019c1f504b4732e973645a2ed08')
        self.assertEqual(self.hash_sha1(tci['audit_trail'][1]['notes']), '013ea81644eec24389fdd9eb0237ecac249dbc1d')
        self.assertEqual(self.hash_sha1(tci['audit_trail'][1]['date']), 'dc0a40c2ece50e2453573393367982418b5507a6')

    def test_internal_charges(self):
        ic = finance_parsers.InternalChargesParser(self.eactivities)
        icl = ic.list(test_club_id, self.year)

        self.assertEqual(len(icl), 21)
        charged_icl = [x for x in icl if unicode(x['charged_committee']['id']) == u'411']
        receiving_icl = [x for x in icl if unicode(x['receiving_committee']['id']) == u'411']
        self.assertEqual(len(charged_icl), 7)
        self.assertEqual(len(receiving_icl), 14)
        self.assertItemsEqual([x['id'] for x in icl], [
            u'718', u'825', u'882', u'930', u'986', u'1036', u'1194',
            u'745', u'759', u'846', u'960', u'964', u'1066', u'1067', u'1115',
            u'1167', u'1198', u'1390', u'1391', u'1463', u'1466'
        ])

        charged_icl_item = charged_icl[0]
        self.assertEqual(charged_icl_item['id'], u'718')
        self.assertEqual(charged_icl_item['receiving_committee']['id'], u'310')
        self.assertEqual(charged_icl_item['receiving_committee']['name'], u'OSC Iranian')
        self.assertEqual(charged_icl_item['charged_committee']['id'], u'411')
        self.assertEqual(charged_icl_item['charged_committee']['name'], u'A&E ICU Cinema')
        self.assertEqual(charged_icl_item['status'], u'COMPLETED')
        self.assertEqual(charged_icl_item['gross_amount'], decimal.Decimal('18.33'))

        receiving_icl_item = receiving_icl[0]
        self.assertEqual(receiving_icl_item['id'], u'745')
        self.assertEqual(receiving_icl_item['charged_committee']['id'], u'940')
        self.assertEqual(receiving_icl_item['charged_committee']['name'], u'Graduate Students\' Union Exec')
        self.assertEqual(receiving_icl_item['receiving_committee']['id'], u'411')
        self.assertEqual(receiving_icl_item['receiving_committee']['name'], u'A&E ICU Cinema')
        self.assertEqual(receiving_icl_item['status'], u'COMPLETED')
        self.assertEqual(receiving_icl_item['gross_amount'], decimal.Decimal('232.46'))

        same_attrs = ['id', 'receiving_committee', 'charged_committee', 'status', 'gross_amount']

        charged_ici = ic.item(test_club_id, self.year, charged_icl_item['id'])
        self.assertEqual([charged_ici[y] for y in same_attrs], [charged_icl_item[y] for y in same_attrs])

        self.assertEqual(len(charged_ici['transaction_lines']), 1)
        x = [
            {
                'description': u'Iranian Society Profits from 11/12',
                'account': {'id': u'705', 'name': u'Goods for Resale'},
                'activity': {'id': u'00', 'name': u'General'},
                'funding_source': {'id': u'1', 'name': u'SGI'},
                'value': {'gross': decimal.Decimal('18.33')},
            }
        ]
        self.assertEqual(charged_ici['transaction_lines'], x)

        self.assertEqual(len(charged_ici['audit_trail']), 2)
        self.assertEqual(self.hash_sha1(charged_ici['audit_trail'][0]['role']), 'b97a2e22f06102a21070b943dde8fdbc306ba5cd')
        self.assertEqual(self.hash_sha1(charged_ici['audit_trail'][0]['name']), 'e89487aa73a04416e733ce875c382b89dcc3d7d5')
        self.assertEqual(self.hash_sha1(charged_ici['audit_trail'][0]['notes']), 'e3cb3bc1947d2f6d9c039b1dfe749897b305f72e')
        self.assertEqual(self.hash_sha1(charged_ici['audit_trail'][0]['date']), '23bdced2eb7bff7308cdc50a300d41391aa627af')

        self.assertEqual(self.hash_sha1(charged_ici['audit_trail'][1]['role']), '55cf5ee221a461c8b3db07cb613622ac61403013')
        self.assertEqual(self.hash_sha1(charged_ici['audit_trail'][1]['name']), '33c3bf7adc0ec7a2cbc15e54dc7f138bc90aac14')
        self.assertEqual(self.hash_sha1(charged_ici['audit_trail'][1]['notes']), '1e9ac3b6c2e52729e9b61567eb3c688ecb466cd2')
        self.assertEqual(self.hash_sha1(charged_ici['audit_trail'][1]['date']), 'e2349e9004bddfe3fd79ce781ad9ccf1d95795a2')

        receiving_ici = ic.item(test_club_id, self.year, receiving_icl_item['id'])
        self.assertEqual([receiving_ici[y] for y in same_attrs], [receiving_icl_item[y] for y in same_attrs])

        # let's just assume that parsing receiving ICs works - they're basically identical anyway

    def test_members_funds_redistributions(self):
        mf = finance_parsers.MembersFundsRedistributionsParser(self.eactivities)
        mfl = mf.list(test_club_id, self.year)
        self.assertEqual(len(mfl), 4)

        mfl_item = mfl[-1]
        self.assertEqual(mfl_item['id'], u'25')
        self.assertEqual(self.hash_sha1(mfl_item['person']), 'fe415757c4183ce3edcac2b560cabcc755b71068')
        self.assertEqual(mfl_item['status'], u'COMPLETED')
        self.assertEqual(mfl_item['funding_source'], {'id': u'1', 'name': u'SGI'})
        self.assertEqual(mfl_item['gross_amount'], decimal.Decimal('97.05'))

        mfi = mf.item(test_club_id, self.year, mfl_item['id'])
        attrs = ['id', 'status', 'funding_source', 'gross_amount']
        self.assertEqual([mfi[x] for x in attrs], [mfl_item[x] for x in attrs])
        self.assertEqual(self.hash_sha1(mfi['person']), self.hash_sha1(mfl_item['person']))
        self.assertEqual(self.hash_sha1(mfi['notes']), '9fc3f57b406a90f37aca3c7b727df08151c4cd22')

        x = [
            {
                'description': u'Zero Winter All-Nighter 2011',
                'account': {
                    'id': u'225', 'name': u'Members Funds'
                },
                'activity': {
                    'id': u'00', 'name': u'General'
                },
                'value': {'gross': decimal.Decimal('97.05')}
            }
        ]
        self.assertEqual(mfi['from_transaction_lines'], x)

        x = [
            {
                'description': u'Zero Winter All-Nighter 2011',
                'account': {
                    'id': u'225', 'name': u'Members Funds'
                },
                'activity': {
                    'id': u'52', 'name': u'Winter All-Nighter'
                },
                'value': {'gross': decimal.Decimal('97.05')}
            }
        ]
        self.assertEqual(mfi['to_transaction_lines'], x)

        self.assertEqual(len(mfi['audit_trail']), 4)
        self.assertEqual(self.hash_sha1(mfi['audit_trail'][0]['role']), '70f7b048909aab7189f17304a27c8a23618d772b')
        self.assertEqual(self.hash_sha1(mfi['audit_trail'][0]['name']), 'fe415757c4183ce3edcac2b560cabcc755b71068')
        self.assertEqual(self.hash_sha1(mfi['audit_trail'][0]['notes']), 'da72a37e76622b97097edf51005241526d331e98')
        self.assertEqual(self.hash_sha1(mfi['audit_trail'][0]['date']), '770113b110933276e9008294f3fbf61cd6e54fce')

        self.assertEqual(self.hash_sha1(mfi['audit_trail'][1]['role']), '55cf5ee221a461c8b3db07cb613622ac61403013')
        self.assertEqual(self.hash_sha1(mfi['audit_trail'][1]['name']), '33c3bf7adc0ec7a2cbc15e54dc7f138bc90aac14')
        self.assertEqual(self.hash_sha1(mfi['audit_trail'][1]['notes']), 'ff9d7c269b39a38fd63840d6828282086e986a2f')
        self.assertEqual(self.hash_sha1(mfi['audit_trail'][1]['date']), '770113b110933276e9008294f3fbf61cd6e54fce')

        self.assertEqual(self.hash_sha1(mfi['audit_trail'][2]['role']), 'e2cf8b0754d2be61073416142f53a7cde5669bfc')
        self.assertEqual(self.hash_sha1(mfi['audit_trail'][2]['name']), 'e77601345ce74019c1f504b4732e973645a2ed08')
        self.assertEqual(self.hash_sha1(mfi['audit_trail'][2]['notes']), '6b5520e300c5773f7271909970eab0e51c601a20')
        self.assertEqual(self.hash_sha1(mfi['audit_trail'][2]['date']), '8613fbaf49fe1d1f92e7e2553dee79ca33f0dc36')

        self.assertEqual(self.hash_sha1(mfi['audit_trail'][3]['role']), 'eb1bbf54e18997a7184c5ebd5c032ad73dbd3ada')
        self.assertEqual(self.hash_sha1(mfi['audit_trail'][3]['name']), 'e64b0c874b103f39164ca6b627a4ab354b9824bf')
        self.assertEqual(self.hash_sha1(mfi['audit_trail'][3]['notes']), '35aa85641b9625e10d8bd8644c570ee869514059')
        self.assertEqual(self.hash_sha1(mfi['audit_trail'][3]['date']), '8613fbaf49fe1d1f92e7e2553dee79ca33f0dc36')

    def test_funding_redistributions(self):
        fr = finance_parsers.FundingRedistributionsParser(self.eactivities)
        frl = fr.list(test_club_id, self.year)
        self.assertEqual(len(frl), 1)

        frl_item = frl[0]
        self.assertEqual(frl_item['id'], u'560')
        self.assertEqual(frl_item['status'], u'COMPLETED')
        self.assertEqual(frl_item['funding_source'], {'id': u'1', 'name': u'SGI'})
        self.assertEqual(frl_item['gross_amount'], decimal.Decimal('610.00'))

        fri = fr.item(test_club_id, self.year, frl_item['id'])
        attrs = ['id', 'status', 'funding_source', 'gross_amount']
        self.assertEqual([fri[x] for x in attrs], [frl_item[x] for x in attrs])

        x = [
            {
                'description': u'Zero cancelled POs from last year',
                'account': {
                    'id': u'725', 'name': u'Copyright & Royalties'
                },
                'activity': {
                    'id': u'52', 'name': u'Winter All-Nighter'
                },
                'value': {'gross': decimal.Decimal('610.00')}
            }
        ]
        self.assertEqual(fri['from_transaction_lines'], x)

        x = [
            {
                'description': u"This has nothing to do with Acts - it's just a place to dump surplus from copyright last year.",
                'account': {
                    'id': u'600', 'name': u'Acts'
                },
                'activity': {
                    'id': u'00', 'name': u'General'
                },
                'value': {'gross': decimal.Decimal('610.00')}
            }
        ]
        self.assertEqual(fri['to_transaction_lines'], x)

        self.assertEqual(len(fri['audit_trail']), 3)
        self.assertEqual(self.hash_sha1(fri['audit_trail'][0]['role']), '70f7b048909aab7189f17304a27c8a23618d772b')
        self.assertEqual(self.hash_sha1(fri['audit_trail'][0]['name']), 'fe415757c4183ce3edcac2b560cabcc755b71068')
        self.assertEqual(self.hash_sha1(fri['audit_trail'][0]['notes']), '83ab746df7203f0f7cb1920913dd42d3959910ce')
        self.assertEqual(self.hash_sha1(fri['audit_trail'][0]['date']), '770113b110933276e9008294f3fbf61cd6e54fce')

        self.assertEqual(self.hash_sha1(fri['audit_trail'][1]['role']), '55cf5ee221a461c8b3db07cb613622ac61403013')
        self.assertEqual(self.hash_sha1(fri['audit_trail'][1]['name']), '33c3bf7adc0ec7a2cbc15e54dc7f138bc90aac14')
        self.assertEqual(self.hash_sha1(fri['audit_trail'][1]['notes']), '17832243bf859adb32ed4a1e7ed051ab4ecba9a3')
        self.assertEqual(self.hash_sha1(fri['audit_trail'][1]['date']), '770113b110933276e9008294f3fbf61cd6e54fce')

        self.assertEqual(self.hash_sha1(fri['audit_trail'][2]['role']), 'e2cf8b0754d2be61073416142f53a7cde5669bfc')
        self.assertEqual(self.hash_sha1(fri['audit_trail'][2]['name']), 'e77601345ce74019c1f504b4732e973645a2ed08')
        self.assertEqual(self.hash_sha1(fri['audit_trail'][2]['notes']), '017af4fcc9114597726ba9fbcf7f9bc94f4e5d60')
        self.assertEqual(self.hash_sha1(fri['audit_trail'][2]['date']), '8613fbaf49fe1d1f92e7e2553dee79ca33f0dc36')
