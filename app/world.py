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

    def _get_top_players(self, count, valuefunc):
        players = [(player.username, valuefunc(player)) for player in self.players]
        return sorted(players, key=lambda player: player[1], reverse=True)[0:count]

    def players_most_online(self, count):
        valuefunc = lambda player: player.data['stat']['playOneMinute']
        return self._get_top_players(count, valuefunc)

    def players_most_broken_blocks(self, count):
        valuefunc = lambda player: sum(player.data['stat']['mineBlock'].values())
        return self._get_top_players(count, valuefunc)

    def players_greatest_distance(self, count):
        valuefunc = lambda player: sum([value for key, value in player.data['stat'].iteritems() if key[-5:] == 'OneCm'])/1000
        return self._get_top_players(count, valuefunc)
