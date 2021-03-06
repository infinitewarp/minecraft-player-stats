import os

from mcstats import cache, config
from mcstats.player import load_players


class World(object):
    """
    Representation of a Minecraft World insofar as it is conceptually
    a collection of Players and their stats within that world.
    """
    def __init__(self):
        self.players = self._load_all_players()

    @cache.cache('world_load_all_players', expire=300)
    def _load_all_players(self):
        filepaths = []
        for filename in os.listdir(config.STATS_DIR_PATH):
            if filename.endswith('.json') and len(filename) > 5:
                filepaths.append(os.path.join(config.STATS_DIR_PATH, filename))

        players = load_players(filepaths)
        return dict([(player.username, player) for player in players])

    def _get_top_players(self, count, valuefunc):
        players = [(username, valuefunc(player)) for username, player in self.players.items()]
        return sorted(players, key=lambda player: player[1], reverse=True)[0:count]

    @property
    def total_mob_kills(self):
        return sum(sum(kill[1] for kill in player.kills) for player in self.players.values())

    @property
    def total_player_deaths(self):
        return sum(player.deaths for player in self.players.values())

    @property
    def total_minutes_played(self):
        return sum(player.data['stat']['playOneMinute'] / 1000 for player in self.players.values())

    @property
    def total_blocks_broken(self):
        return sum(sum(player.data['stat']['mineBlock'].values()) for player in self.players.values())

    def players_most_online(self, count):
        def valuefunc(player):
            return player.play_time_minutes
        return self._get_top_players(count, valuefunc)

    def players_most_broken_blocks(self, count):
        def valuefunc(player):
            return sum(player.data['stat']['mineBlock'].values())
        return self._get_top_players(count, valuefunc)

    def players_most_crafted_items(self, count):
        def valuefunc(player):
            return sum(player.data['stat']['craftItem'].values())
        return self._get_top_players(count, valuefunc)

    def players_greatest_distance(self, count):
        def valuefunc(player):
            return sum([value for key, value in player.data['stat'].items() if key.endswith('OneCm')]) / 1000
        return self._get_top_players(count, valuefunc)

    def players_most_kills(self, count):
        def valuefunc(player):
            return sum(kill[1] for kill in player.kills)
        return self._get_top_players(count, valuefunc)

    def players_most_deaths(self, count):
        def valuefunc(player):
            return player.deaths
        return self._get_top_players(count, valuefunc)

    def usernames(self):
        return sorted(self.players.keys(), key=lambda username: username.lower())
