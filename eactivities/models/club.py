from . import Model, LazyModelMixin
from .documentation import Documentation
from .finances import Finances
from eactivities.parsers.club import ClubParser


class ClubMembership(Model):
    _attributes = [
        'full_members', 'full_members_quota',
        'membership_cost', 'associate_members'
    ]


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
