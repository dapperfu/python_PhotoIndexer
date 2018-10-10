
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

import os
import cached_property
from .redis_db import load_databases
from .redis_cache import RedisCacheMixin, CacherMixin

class MediaIndexer(RedisCacheMixin, CacherMixin):
    def __init__(self, config):
        self.config=config
        
    @cached_property.cached_property
    def databases(self):
        return load_databases(self.config)
    
        
    def __repr__(self):
        return "MediaIndexer<{}>".format(os.path.basename(self.config))
        

    def flush_keys(self):
        databases = self.databases
        for db_name, db in databases.items():
            print("{} db: flushing".format(db_name))


    def key_count(self):
        databases = self.databases
        for db_name, db in databases.items():
            print("{} db: {} keys".format(db_name, db.dbsize()))