import unittest
import decimal
import os
import datetime
import hashlib

from nose.plugins.attrib import attr

from eactivities import EActivities

# loading secrets from environment!
username = os.getenv('EHACK_TEST_USERNAME')
password = os.getenv('EHACK_TEST_PASSWORD')
test_club_id = int(os.getenv('EHACK_TEST_CLUB', '0'))

credentials = username is not None and password is not None and test_club_id
my__eactivities = None


def setup():
    global my__eactivities

    if not credentials:
        raise unittest.SkipTest("EHACK_TEST_* environment variables missing")

    my__eactivities = EActivities(credentials=(username, password.decode('base64')))


def teardown():
    global my__eactivities

    my__eactivities.logout()


@attr('live')
class EActivitiesBaseTestCase(unittest.TestCase):
    def setUp(self):
        global my__eactivities

        self.eactivities = my__eactivities


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
        self.assertIsNotNone(self.club.members)
        self.assertItemsEqual(self.club.members.keys(), [
            'full_members', 'full_members_quota',
            'associate_members', 'membership_cost'
        ])

    def test_not_visible(self):
        self.club = self.eactivities.club(406)  # just hope leosoc never use this
        with self.assertRaises(AttributeError):
            self.club.active
        with self.assertRaises(AttributeError):
            self.club.email
        with self.assertRaises(AttributeError):
            self.club.current_profile_entry
        self.assertIsNotNone(self.club.members)
        self.assertItemsEqual(self.club.members.keys(), [
            'full_members', 'full_members_quota',
            'associate_members', 'membership_cost'
        ])


class ClubDocumentationTestCase(ClubBaseTestCase):
    def setUp(self):
        super(ClubDocumentationTestCase, self).setUp()

        self.documentation = self.club.documentation()

    def test_inventory(self):
        inventory = self.documentation.inventory()

        inv_list = inventory.list()

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
        risk_assessment = self.documentation.risk_assessment()

        ra_list = risk_assessment.list()

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
        key_lists = self.documentation.key_lists()

        kls = key_lists.list()

        for key_list in kls:
            self.assertIn('id', key_list)

            key_list_item = key_lists.item(key_list['id'])
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

    def test_overview(self):
        fo = self.f.funding_overview
        self.assertGreater(len(fo), 1)

    def test_banking_records(self):
        br = self.f.banking_records()
        brl = br.list()

        if len(brl) > 0:
            brl_zero = brl[0]
            brl_zero_item = br.item(brl_zero['id'])
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

            br.pdf(brl_zero_item['id'], brl_zero_item['paying_in_slips'][0])

    def test_sales_invoices(self):
        si = self.f.sales_invoices()
        sil = si.list()

        if len(sil) > 0:
            sil_zero = sil[0]
            sil_zero_item = si.item(sil_zero['id'])
            self.assertEqual(sil_zero['id'], sil_zero_item['id'])
            self.assertEqual(sil_zero['date'], sil_zero_item['date'])
            self.assertEqual(sil_zero['customer']['name'], sil_zero_item['customer']['name'])
            self.assertEqual(sil_zero['po_number'], sil_zero_item['customer_purchase_order_number'])
            self.assertEqual(sil_zero['gross_amount'], sil_zero_item['gross_amount'])

            self.assertItemsEqual(sil_zero.keys(), [
                'id', 'date', 'customer', 'po_number', 'gross_amount'
            ])
            self.assertItemsEqual(sil_zero_item.keys(), [
                'id', 'date', 'customer', 'international',
                'customer_purchase_order_number', 'audit_trail',
                'next_authorisers', 'transaction_lines',
                'gross_amount', 'purchase_order_attachments'
            ])

            si.item_pdf(sil_zero_item['id'])

            if len(sil_zero_item['purchase_order_attachments']) > 1:
                si.pdf(sil_zero_item['id'], sil_zero_item['purchase_order_attachments'][0])

    def test_claims(self):
        cl = self.f.claims()
        cll = cl.list()

        if len(cll) > 0:
            cll_zero = cll[0]
            cll_zero_item = cl.item(cll_zero['id'])
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
                cl.pdf(cll_zero_item['id'], cll_zero_item['receipts'][0])

    def test_purchase_orders(self):
        po = self.f.purchase_orders()
        pol = po.list()

        if len(pol) > 0:
            pol_zero = pol[0]
            pol_zero_item = po.item(pol_zero['id'])
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
                po.pdf(pol_zero_item['id'], pol_zero_item['invoices'][0])

    def test_transaction_corrections(self):
        tc = self.f.transaction_corrections()
        tcl = tc.list()

        if len(tcl) > 0:
            tcl_zero = tcl[0]
            tcl_zero_item = tc.item(tcl_zero['id'])
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
        ic = self.f.internal_charges()
        icl = ic.list()

        if len(icl) > 0:
            icl_zero = icl[0]
            icl_zero_item = ic.item(icl_zero['id'])
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
        mfr = self.f.members_funds_redistributions()
        mfrl = mfr.list()

        if len(mfrl) > 0:
            mfrl_zero = mfrl[0]
            mfrl_zero_item = mfr.item(mfrl_zero['id'])
            self.assertEqual(mfrl_zero['id'], mfrl_zero_item['id'])
            self.assertEqual(mfrl_zero['person'], mfrl_zero_item['person'])
            self.assertEqual(mfrl_zero['status'], mfrl_zero_item['status'])
            self.assertEqual(mfrl_zero['funding'], mfrl_zero_item['funding'])
            self.assertEqual(mfrl_zero['gross_amount'], mfrl_zero_item['gross_amount'])

            self.assertItemsEqual(mfrl_zero.keys(), [
                'id', 'person', 'status', 'funding', 'gross_amount'
            ])
            self.assertItemsEqual(mfrl_zero_item.keys(), [
                'id', 'person', 'funding', 'gross_amount', 'notes',
                'status', 'audit_trail', 'next_authorisers', 'from_transaction_lines',
                'to_transaction_lines'
            ])


class ClubFinanceCinemaTestCase(ClubBaseTestCase):
    def setUp(self):
        super(ClubFinanceCinemaTestCase, self).setUp()

        if test_club_id != 411:
            raise unittest.SkipTest("results stored only for 411")

        self.f = self.club.finances(2012)

    def fetch_sha1(self, thing):
        s = hashlib.sha1()
        for chunk in thing.iter_content(1024):
            s.update(chunk)
        return s.hexdigest()

    def test_overview(self):
        fo = self.f.funding_overview
        self.assertEqual(len(fo), 3)
        self.assertEqual(fo['Grant (0)'], decimal.Decimal('0'))
        self.assertEqual(fo['SGI (1)'], decimal.Decimal('-3964.64'))
        self.assertEqual(fo['Harlington (2)'], decimal.Decimal('-13095.89'))

    def test_banking_records(self):
        br = self.f.banking_records()
        brl = br.list()
        self.assertEqual(len(brl), 11)
        self.assertItemsEqual([x['id'] for x in brl], [
            u'124830', u'124831', u'124832', u'124833', u'124834', u'124835', u'124836',
            u'141013', u'141014', u'141015', u'141016'
        ])
        br_x = [x['gross_amount'] for x in brl if x['id'] == u'124830'][0]
        self.assertEqual(br_x, decimal.Decimal('606.33'))

        bri = br.item(u'124830')
        self.assertEqual(bri['date'], datetime.date(2012, 10, 16))
        self.assertEqual(len(bri['transaction_lines']), 5)
        self.assertEqual(self.fetch_sha1(br.pdf(bri['id'], bri['paying_in_slips'][0])), 'a5ba9d8b9efca6f593d7af5046c9fe7de32c7b09')

    def test_sales_invoices(self):
        si = self.f.sales_invoices()
        sil = si.list()
        self.assertEqual(len(sil), 1)
        self.assertItemsEqual([x['id'] for x in sil], [u'602067'])

        sii = si.item(u'602067')
        self.assertEqual(sii['date'], datetime.date(2013, 6, 25))
        self.assertEqual(self.fetch_sha1(si.pdf(sii['id'], sii['purchase_order_attachments'][0])), 'cc9ccb9807694f654aed6ddd590ac404d40ca3e0')
