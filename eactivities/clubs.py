# vim: set fileencoding=utf-8

from . import exceptions, club_finances, club_documentation, utils


class Club(object):
    def __init__(self, eactivities, club_id):
        self.eactivities = eactivities
        self.id = club_id
        self.name = self.fetch_name()

        self.loaded_data = False

    def __getattr__(self, name):
        if not self.loaded_data:
            for k, v in self.load_data().iteritems():
                setattr(self, k, v)
            self.loaded_data = True

        return super(Club, self).__getattribute__(name)

    def fetch_name(self):
        soup, _ = self.eactivities.load_and_start(
            '/finance/transactions/{}'.format(self.id)
        )

        title = unicode(soup.find('xmlcurrenttitle').get_text())
        if title == 'NO RECORDS':
            raise Club.DoesNotExist("No financial records available for club")
        elif '(' not in title:
            raise exceptions.EActivitiesHasChanged(
                'No ( found in club - has format changed?'
            )

        name, club_id = utils.split_role(title)
        assert club_id == unicode(self.id)

        return name

    def pick_best_role(self):
        best_roles = []
        for role in self.eactivities.roles().values():
            if role['committee'].upper() == self.name:
                self.name = role['committee']  # don't mind me...
                if role['position'] == 'Member':
                    best_roles.append(role)
                else:
                    best_roles.insert(0, role)
        if len(best_roles) == 0:
            return None
        return best_roles[0]

    def load_data(self):
        info = {
            'id': self.id,
            'name': self.name
        }

        # try and load admin/csp/details
        details_soup, _ = self.eactivities.load_and_start(
            '/admin/csp/details/{}'.format(self.id)
        )
        if details_soup.xmlcurrenttitle.get_text() != 'NO RECORDS':
            # hooray!
            details_dict = {}
            details_bits = details_soup.find("enclosure", id="392")
            for details_label in details_bits.find_all("label"):
                details_value = details_label.find_next_sibling(
                    "infoenclosure"
                )
                details_dict[unicode(details_label.get_text())] = {
                    'label': details_label,
                    'value': details_value
                }

            info['active'] = details_dict['STATUS']['value'].get_text().strip() \
                == 'Active'
            website = details_dict['WEBSITE']['value'].find("infofield")
            info['website'] = unicode(
                website.attrs['link'] + website.get_text().strip()
            )
            info['email'] = unicode(
                details_dict['EMAIL']['value'].get_text().strip() + '@imperial.ac.uk'
            )
            info['current_profile_entry'] = [
                unicode(x.get_text().strip())
                for x in
                details_dict['CURRENT PROFILE ENTRY']['value'].find_all(
                    'infofield'
                )
            ]

            # now for membership
            membership_soup, _ = self.eactivities.ajax_handler({
                'ajax': 'activatetabs', 'navigate': '395'
            })
            membership = {}

            _, _, full_members_bit = membership_soup.find(
                "infofield", id="354-0"
            ).get_text().partition(': ')
            full_members_bit, _, _ = full_members_bit.partition(' (')
            full_members, _, membership_quota = full_members_bit.partition(
                ' of '
            )
            membership['full_members'] = int(full_members)
            membership['full_members_quota'] = int(membership_quota)

            _, _, membership_costs = membership_soup.find(
                "infofield", id="354-1"
            ).get_text().partition(' costs ')
            membership['membership_cost'] = utils.format_price(
                membership_costs
            )

            membership['associate_members'] = 0
            associate_members_bit = membership_soup.find(
                "infofield", id="355-0"
            )
            if associate_members_bit:
                am_str = associate_members_bit.get_text()
                _, _, associate_members = am_str.partition(': ')
                membership['associate_members'] = int(associate_members)

            info['members'] = membership
        else:
            # try their financials page for the membership info?
            membership_soup, _ = self.eactivities.load_and_start(
                '/finance/transactions/{}'.format(self.id)
            )
            membership = {}

            _, _, full_members_bit = membership_soup.find(
                "infofield", alias="MemDetails"
            ).get_text().partition(': ')
            full_members_bit, _, _ = full_members_bit.partition(' (')
            full_members, _, membership_quota = full_members_bit.partition(
                ' of '
            )
            membership['full_members'] = int(full_members)
            membership['full_members_quota'] = int(membership_quota)

            _, _, membership_costs = membership_soup.find(
                "infofield", alias="YearDetails"
            ).get_text().partition(' costs ')
            membership['membership_cost'] = utils.format_price(
                membership_costs
            )

            membership['associate_members'] = 0
            associate_members_bit = membership_soup.find(
                "infofield", alias="MemNum"
            )
            if associate_members_bit:
                am_str = associate_members_bit.get_text()
                _, _, associate_members = am_str.partition(': ')
                membership['associate_members'] = int(associate_members)

            info['members'] = membership

        return info

    def finances(self, year):
        return club_finances.ClubFinances(self, year)

    def documentation(self):
        return club_documentation.ClubDocumentation(self)

    class DoesNotExist(exceptions.DoesNotExist):
        pass
