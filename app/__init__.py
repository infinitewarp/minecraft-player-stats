from flask import Flask
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/minecraft-player-stats/data',
    'cache.lock_dir': '/tmp/minecraft-player-stats/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

app = Flask(__name__)

# Python linters will complain about the next line. It's OK! Ignore them.
from app import views
