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
        stats_dir = os.path.join(config.MINECRAFT_WORLD_DIR_PATH, 'stats')
        for filename in os.listdir(stats_dir):
            if filename[-5:] == '.json' and len(filename) > 5:
                fullpath = os.path.join(stats_dir, filename)
                self.players.append(Player(filepath=fullpath))
