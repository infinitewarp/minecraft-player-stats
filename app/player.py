import os
import json
import config
from util import tree


class IllegalAccessException(Exception):
    pass


class Player(object):
    """
    Representation of a player based on his stats.
    """
    def __init__(self, username=None, filepath=None):
        if username:
            self.username = username
            self.filepath = self._filepath_from_username(username)
        elif filepath:
            self.filepath = filepath
            self.username = self._username_from_filepath(filepath)
        self.data = tree()
        self._load()

    def _filepath_from_username(self, username):
        # eg. "/foo/bar/minecraft/world/stats/notch.json"
        return os.path.join(config.STATS_DIR_PATH, username + '.json')

    def _username_from_filepath(self, filepath):
        # eg. "/foo/bar/minecraft/world/stats/notch.json"
        return os.path.split(filepath)[-1][:-5]

    def _load(self):
        """
        Load the player's stats data from disk.
        """
        if '..' in self.filepath:
            # Don't let someone try to walk up the path!
            # TODO Is there a better way to do this?
            raise IllegalAccessException("Illegal access to: %s" % self.filepath)
        with open(self.filepath, 'r') as f:
            data = json.load(f)
            for key, value in data.iteritems():
                self._load_stat(key, value)

    def _load_stat(self, key, value):
        """
        Load this single stat into the data tree.
        """
        subkeys = key.split('.')
        node = self.data
        for subkey in subkeys[0:-1]:
            if subkey not in node:
                node[subkey]
            node = node[subkey]
        node[subkeys[-1]] = value
