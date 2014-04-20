from threading import Thread
import json
import os
import re

from mcstats.misc import ACHIEVEMENT_NAMES, ENTITY_NAMES
from mcstats.profile import Profile
from mcstats.util import tree


class Player(object):

    """Representation of a player based on his stats."""

    def __init__(self, filepath):
        self.data = tree()
        profile = self._fetch_profile(filepath)
        if profile:
            self.uuid = profile.uuid
            self.username = profile.username
            self._load(filepath)

    def _fetch_profile(self, filepath):
        name, is_uuid = self._extract_filename(filepath)
        return Profile(uuid=name) if is_uuid else Profile(username=name)

    def _extract_filename(self, filepath):
        """Extract a name from the path and determine if it's a UUID."""
        name = os.path.split(filepath)[-1][:-5].replace('-', '').lower()
        is_uuid = re.match('[0-9a-f]{32}', name) is not None
        return name, is_uuid

    def _load(self, filepath):
        """Load the player's stats data from disk."""
        with open(filepath, 'r') as f:
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
        """Return the achievements this player has, err, achieved."""
        def is_met(value):
            if isinstance(value, int) and value > 0:
                return True
            return value['value'] > 0

        achievements = [ACHIEVEMENT_NAMES[name] for name, value in self.data['achievement'].items() if is_met(value)]
        # TODO Should achievements have a special non-alphabetic sort?
        return sorted(achievements)

    @property
    def kills(self):
        """Return the names and counts of entities this player has killed."""
        entities = [(ENTITY_NAMES[name], value) for name, value in self.data['stat']['killEntity'].items()]
        return sorted(entities, key=lambda entity: entity[1], reverse=True)

    @property
    def deaths(self):
        """Return the number of deaths for this player."""
        return self.data['stat']['deaths'] if isinstance(self.data['stat']['deaths'], int) else 0

    @property
    def play_time_minutes(self):
        # Weird bug in minecraft! Even though the stat says "playOneMinute",
        # the value is the time in milliminutes. Yes, you read that right.
        return self.data['stat']['playOneMinute'] / 1000

    @property
    def killed_by(self):
        """Return the names and counts of entities that have killed this player."""
        entities = [(ENTITY_NAMES[name], value) for name, value in self.data['stat']['entityKilledBy'].items()]
        return sorted(entities, key=lambda entity: entity[1], reverse=True)


def load_players(filepaths):
    """
    Get a list of Players from a list of filepaths.
    """
    threads = []
    for filepath in filepaths:
        thread = PlayerLoaderThread(filepath)
        thread.start()
        threads.append(thread)

    players = []
    for thread in threads:
        thread.join()
        if thread.player:
            players.append(thread.player)

    return players


class PlayerLoaderThread(Thread):
    """
    Custom thread to speed up the loading of Player data in parallel because
    serially requesting data from Mojang for many players can be very slow.
    """
    def __init__(self, filepath):
        super(PlayerLoaderThread, self).__init__()
        self.filepath = filepath
        self.player = None

    def run(self):
        self.player = Player(self.filepath)
