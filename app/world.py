import os
import config
from player import Player


class World(object):
    """
    Representation of a Minecraft World insofar as it is conceptually
    a collection of Players and their stats within that world.
    """
    def __init__(self):
        self.players = []
        self._load_all_players()

    def _load_all_players(self):
        for filename in os.listdir(config.STATS_DIR_PATH):
            if filename[-5:] == '.json' and len(filename) > 5:
                fullpath = os.path.join(config.STATS_DIR_PATH, filename)
                self.players.append(Player(filepath=fullpath))
