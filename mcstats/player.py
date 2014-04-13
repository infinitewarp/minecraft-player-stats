import json
import os

from mcstats import config
from mcstats.misc import ACHIEVEMENT_NAMES, ENTITY_NAMES
from mcstats.util import tree


class IllegalFileAccessError(IOError):
    pass


class Player(object):

    """Representation of a player based on his stats."""

    def __init__(self, username=None, filepath=None):
        if username:
            self.username = username
            self.filepath = self._filepath_from_username(username)
        elif filepath:
            self.filepath = filepath
            self.username = self._username_from_filepath(filepath)
        self.data = tree()
        if getattr(self, 'filepath', None):
            self._load()

    def _filepath_from_username(self, username):
        """Derive the filepath from the username.

        >>> orig, config.STATS_DIR_PATH = config.STATS_DIR_PATH, '/foo/bar/'
        >>> player = Player()
        >>> player._filepath_from_username('notch')
        '/foo/bar/notch.json'

        >>> import pytest
        >>> pytest.raises(IOError, player._filepath_from_username, '../notch')
        <ExceptionInfo IllegalFileAccessError tblen=2>

        >>> config.STATS_DIR_PATH = orig
        """
        if len(os.path.split(username)[0]) > 1:
            raise IllegalFileAccessError()
        return os.path.join(config.STATS_DIR_PATH, username + '.json')

    def _username_from_filepath(self, filepath):
        """Derive the username from the filepath.

        >>> player = Player()
        >>> player._username_from_filepath('/tmp/world/stats/notch.json')
        'notch'
        """
        return os.path.split(filepath)[-1][:-5]

    def _load(self):
        """Load the player's stats data from disk."""
        with open(self.filepath, 'r') as f:
            data = json.load(f)
            for key, value in data.items():
                self._load_stat(key, value)

    def _load_stat(self, key, value):
        """Load this single stat into the data tree."""
        subkeys = key.split('.')
        node = self.data
        for subkey in subkeys[0:-1]:
            if subkey not in node:
                node[subkey]
            node = node[subkey]
        node[subkeys[-1]] = value

    @property
    def achievements(self):
        """Return the achievements this player has, err, achieved.

        >>> player = Player()
        >>> player._load_stat('achievement.killEnemy', 769)
        >>> player._load_stat('achievement.buildWorkBench', 4)
        >>> player._load_stat('achievement.mineWood', 2271)
        >>> player._load_stat('achievement.exploreAllBiomes', {'value': 0})
        >>> player.achievements
        ['Benchmarking', 'Getting Wood', 'Monster Hunter']

        >>> player = Player()
        >>> player._load_stat('achievement.exploreAllBiomes', {'value': 1})
        >>> player.achievements
        ['Adventuring Time']
        """
        def is_met(value):
            if isinstance(value, int) and value > 0:
                return True
            return value['value'] > 0

        achievements = [ACHIEVEMENT_NAMES[name] for name, value in self.data['achievement'].items() if is_met(value)]
        # TODO Should achievements have a special non-alphabetic sort?
        return sorted(achievements)

    @property
    def kills(self):
        """Return the names and counts of entities this player has killed.

        >>> player = Player()
        >>> player._load_stat('stat.killEntity.Cow', 5)
        >>> player._load_stat('stat.killEntity.Pig', 23)
        >>> player._load_stat('stat.killEntity.Sheep', 21)
        >>> player.kills
        [('Pig', 23), ('Sheep', 21), ('Cow', 5)]
        """
        entities = [(ENTITY_NAMES[name], value) for name, value in self.data['stat']['killEntity'].items()]
        return sorted(entities, key=lambda entity: entity[1], reverse=True)

    @property
    def killed_by(self):
        """Return the names and counts of entities that have killed this player.

        >>> player = Player()
        >>> player._load_stat('stat.entityKilledBy.Creeper', 5)
        >>> player._load_stat('stat.entityKilledBy.Skeleton', 23)
        >>> player._load_stat('stat.entityKilledBy.Zombie', 21)
        >>> player.killed_by
        [('Skeleton', 23), ('Zombie', 21), ('Creeper', 5)]
        """
        entities = [(ENTITY_NAMES[name], value) for name, value in self.data['stat']['entityKilledBy'].items()]
        return sorted(entities, key=lambda entity: entity[1], reverse=True)
