from . import Model, LazyModelMixin, ArrayModel
from .documentation import Documentation
from .finances import Finances
from eactivities.parsers.club import ClubParser, MembersListParser


def collapse_key_list_data(raw_members_list_data, key_list_data):
    # TODO: collapse key_list_data into members list
    return raw_members_list_data


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

    def list(self, augmented=False):
        data = MembersListParser.fetch(self._eactivities, id=self._parent.id)

        if augmented:
            data = collapse_key_list_data(
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
