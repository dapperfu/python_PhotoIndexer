
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

import os
import cached_property

class MediaIndexer(object):
    def __init__(self, config):
        self.config=config
        
    
        
        
    def __repr__(self):
        return "MediaIndexer<{}>".format(os.path.basename(self.config))
        