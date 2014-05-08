from . import Model, LazyModelMixin, ArrayModel
from .documentation import Documentation
from .finances import Finances
from eactivities.parsers.club import ClubParser, MembersListParser


def collapse_key_list_data(club_id, raw_members_list_data, key_list_data):
    mld = list(raw_members_list_data)
    cid_data = {}
    for key_list in key_list_data.values():
        for person in key_list.people:
            cid = person.cid
            cid_data.setdefault(
                cid, {'active': {}, 'inactive': {}}
            )['active' if person.active else 'inactive'].setdefault(
                unicode(club_id), []
            ).append(key_list.id)

    for person in mld:
        if person['cid'] in cid_data:
            person['key_list_memberships'] = cid_data[person['cid']]
        else:
            person['key_list_memberships'] = {'active': {}, 'inactive': {}}

    return mld


class ClubMember(Model):
    _attributes = [
        'date', 'order_no', 'cid', 'login',
        'first_name', 'last_name', 'email', 'membership_type'
    ]


class ClubMembersList(ArrayModel):
    _submodel = ClubMember


class ClubMembership(Model):
    _attributes = [
        'full_members', 'full_members_quota',
        'membership_cost', 'associate_members'
    ]

    def list(self, with_key_lists=False):
        data = MembersListParser.fetch(self._eactivities, id=self._parent.id)

        if with_key_lists:
            data = collapse_key_list_data(
                self._parent.id,
                data,
                self._parent.documentation().key_lists()
            )

        return ClubMembersList(eactivities=self._eactivities, data=data, parent=self)


class Club(Model, LazyModelMixin):
    _submodels = {
        'membership': ClubMembership
    }
    _attributes = [
        'id', 'name', 'membership', 'active',
        'website', 'email', 'current_profile_entry'
    ]
    _lazy_loader_parser = ClubParser

    def documentation(self):
        return Documentation(eactivities=self._eactivities, data={'club_id': self.id}, parent=self)

    def finances(self, year):
        return Finances(eactivities=self._eactivities, data={'club_id': self.id, 'year': year}, parent=self)

    def pick_best_role(self):
        best_roles = []
        for role in self._eactivities.roles().values():
            if role['committee'].upper() == self.name:
                self.name = role['committee']  # don't mind me...
                if role['position'] == 'Member':
                    best_roles.append(role)
                else:
                    best_roles.insert(0, role)
        if len(best_roles) == 0:
            return None
        return best_roles[0]
