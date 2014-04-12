import os

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from flask import Flask

from app import config

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': os.path.join(config.TEMP_DIR, 'data'),
    'cache.lock_dir': os.path.join(config.TEMP_DIR, 'lock'),
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

app = Flask(__name__)

# Python linters will complain about the next line. It's OK! Ignore them.
from app import views
