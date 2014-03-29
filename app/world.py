import os
import config
from app import cache
from player import Player


class World(object):
    """
    Representation of a Minecraft World insofar as it is conceptually
    a collection of Players and their stats within that world.
    """
    def __init__(self):
        self.players = self._load_all_players()

    @cache.cache('world_load_all_players', expire=300)
    def _load_all_players(self):
        players = {}
        for filename in os.listdir(config.STATS_DIR_PATH):
            if filename[-5:] == '.json' and len(filename) > 5:
                fullpath = os.path.join(config.STATS_DIR_PATH, filename)
                player = Player(filepath=fullpath)
                players[player.username] = player
        return players

    def _get_top_players(self, count, valuefunc):
        players = [(username, valuefunc(player)) for username, player in self.players.iteritems()]
        return sorted(players, key=lambda player: player[1], reverse=True)[0:count]

    def players_most_online(self, count):
        # Weird bug in minecraft! Even though the stat says "playOneMinute",
        # the value is the time in milliminutes. Yes, you read that right.
        valuefunc = lambda player: player.data['stat']['playOneMinute']/1000
        return self._get_top_players(count, valuefunc)

    def players_most_broken_blocks(self, count):
        valuefunc = lambda player: sum(player.data['stat']['mineBlock'].values())
        return self._get_top_players(count, valuefunc)

    def players_most_crafted_items(self, count):
        valuefunc = lambda player: sum(player.data['stat']['craftItem'].values())
        return self._get_top_players(count, valuefunc)

    def players_greatest_distance(self, count):
        valuefunc = lambda player: sum([value for key, value in player.data['stat'].iteritems() if key[-5:] == 'OneCm'])/1000
        return self._get_top_players(count, valuefunc)

    def players_most_kills(self, count):
        valuefunc = lambda player: sum(kill[1] for kill in player.kills)
        return self._get_top_players(count, valuefunc)

    def players_most_deaths(self, count):
        valuefunc = lambda player: player.data['stat']['deaths'] if isinstance(player.data['stat']['deaths'], int) else 0
        return self._get_top_players(count, valuefunc)

    def usernames(self):
        return sorted(self.players.keys(), key=lambda username: username.lower())
