
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

import os
import cached_property
from .redis_db import load_databases

class MediaIndexer(object):
    def __init__(self, config):
        self.config=config
        
    @cached_property
    
    load_databases
    
        
        
    def __repr__(self):
        return "MediaIndexer<{}>".format(os.path.basename(self.config))
        