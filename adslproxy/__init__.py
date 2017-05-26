__version__ = '0.9.9'
from adslproxy.db import RedisClient
from adslproxy.api import server

def version():
    return __version__

