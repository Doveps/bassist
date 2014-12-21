from . import common
from systems import group

class GroupsStdoutLog(common.Log):

    def parse(self):
        self.logger.debug('parsing')

        self.groups = group.Groups()
        with open(self.path, 'r') as f:
            for line in f.readlines():
                parts = line.rstrip('\n').split(':')
                assert len(parts) is 4

                (group_name, password, gid, users) = parts[0:4]

                assert group_name not in self.groups

                self.groups[group_name] = group.Group(password, gid)

                # avoid setting users to '' if there are no users
                users = users.split(',')
                if len(users) is 1 and users[0] is '': continue

                self.groups[group_name].add_users(users)

    def record(self, flavor):
        self.logger.debug('recording %d groups',len(self.groups))
        flavor.record('groups', self.groups)