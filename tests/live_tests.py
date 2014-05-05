import unittest
import os

from nose.plugins.attrib import attr

from eactivities import EActivities

# loading secrets from environment!
username = os.getenv('EHACKTIVITIES_TEST_USERNAME')
password = os.getenv('EHACKTIVITIES_TEST_PASSWORD')
test_club_id = int(os.getenv('EHACKTIVITIES_TEST_CLUB', '0'))

credentials = username is not None and password is not None and test_club_id


def setup():
    if not credentials:
        raise unittest.SkipTest("EHACKTIVITIES_TEST_* environment variables missing")


@attr('live')
class EActivitiesBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.eactivities = EActivities(credentials=(username, password))

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
