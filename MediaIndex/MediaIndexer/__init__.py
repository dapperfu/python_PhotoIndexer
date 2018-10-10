
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

import os
import cached_property
from .redis_db import load_databases
from .redis_cache import RedisCacheMixin

class MediaIndexer(RedisCacheMixin, CacherMixin):
    def __init__(self, config):
        self.config=config
        
    @cached_property.cached_property
    def databases(self):
        return load_databases(self.config)
    
        
        
    def __repr__(self):
        return "MediaIndexer<{}>".format(os.path.basename(self.config))
        