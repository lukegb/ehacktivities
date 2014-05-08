from .. import utils, encoding_utils, exceptions
from . import BaseParser


class ClubParser(BaseParser):

    def fetch_data(self, id, **kwargs):
        info = {
            'id': id
        }

        # try and load admin/csp/details
        details_soup, _ = self.eactivities.load_and_start(
            '/admin/csp/details/{}'.format(id)
        )
        if details_soup.xmlcurrenttitle.get_text() != 'NO RECORDS':
            name = unicode(details_soup.xmlcurrenttitle.get_text())
            info['name'], _ = utils.split_role(name)

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
            info['current_profile_entry'] = dict(zip(['short', 'long'], [
                unicode(x.get_text().strip())
                for x in
                details_dict['CURRENT PROFILE ENTRY']['value'].find_all(
                    'infofield'
                )
            ]))

        # try their financials page for the membership info
        membership_soup, _ = self.eactivities.load_and_start(
            '/finance/transactions/{}'.format(id)
        )
        membership = {}

        name = unicode(membership_soup.xmlcurrenttitle.get_text())
        if '(' not in name:
            return None
        info['name'], _ = utils.split_role(name)

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

        info['membership'] = membership

        return info


class MembersListParser(BaseParser):
    def fetch_data(self, id, **kwargs):
        details_soup, _ = self.eactivities.load_and_start(
            '/admin/csp/details/{}'.format(id)
        )

        # click "members"
        members_tab_id = details_soup.find("enclosure", label="Members").attrs['id']
        self.eactivities.activate_tab(details_soup, members_tab_id)

        # download the csv!
        resp = self.eactivities.streaming_get("/admin/csp/details/csv")
        csvr = encoding_utils.EActivitiesCsvReader(resp.raw)

        mode = 'full'
        out = []

        for line in csvr:
            if len(line) == 1 and 'Associate' in line[0]:
                mode = 'associate'
                continue
            elif len(line) <= 1:
                continue
            elif len(line) != 7:
                raise exceptions.EActivitiesHasChanged('CSV format has changed. Again.')
            elif line[0] == 'Date':
                continue

            data = {
                'membership_type': mode
            }
            data['date'], data['order_no'], data['cid'], data['login'], data['first_name'], data['last_name'], data['email'] = line
            data['date'] = utils.parse_date(data['date'])

            out.append(data)

        return out
