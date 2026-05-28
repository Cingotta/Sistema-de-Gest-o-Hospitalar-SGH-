import sqlite3
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DB = os.path.join(_DIR, '..', '..', 'computadores', 'recepcao', 'cache.db')
AUTH_DB = os.path.join(_DIR,'..','recepcao','auth.db')

