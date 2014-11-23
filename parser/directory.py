import os
import logging

from . import host

class ParserDirectoryException(Exception):
    pass

class Directory(object):
    def __init__(self, path):
        self.path = path
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.hosts = []

        for entry in os.listdir(self.path):
            full = os.path.join(self.path, entry)
            self.logger.debug('examining: %s', full)

            if not os.path.isdir(full):
                continue

            self.logger.debug('appending directory')
            self.hosts.append(host.Host(full))
