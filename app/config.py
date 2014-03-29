import os
import tempfile

# TODO get this path from somewhere else?
MINECRAFT_WORLD_DIR_PATH = os.path.expanduser('~/Dropbox/Development/world')
STATS_DIR_PATH = os.path.join(MINECRAFT_WORLD_DIR_PATH, 'stats')

# Replace or supplement these sample links as you see fit.
NAVBAR_LINKS = [
    ('World Map', 'http://my.great.server/map/'),
    ('Server Info', 'http://my.great.server/info.html'),
    ('Join Us!', 'http://my.great.server/join.html'),
]

# This is the name of your server as it will show on the front page
SERVER_NAME = 'My Great Server'

# The app needs to be able to write temporary cache data to disk
TEMP_DIR = os.path.join(tempfile.gettempdir(), 'minecraft-player-stats')
