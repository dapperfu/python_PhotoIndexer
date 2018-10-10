
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

import os
import cached_property
from .redis_utils import load_databases
from .redis_cache import RedisCacheMixin
from .utils import read_config
import pydarknet2

class MediaIndexer(RedisCacheMixin):
    def __init__(self, config_file):
        self.config_file = config_file

    @cached_property.cached_property
    def config(self):
        return read_config(self.config_file)

    @cached_property.cached_property
    def databases(self):
        return load_databases(self.config)

    def __repr__(self):
        return "MediaIndexer<{}>".format(os.path.basename(self.config))

    @cached_property.cached_property
    def classifier(self):
        print("Loading darknet classifier, one minute.")
        return pydarknet2.Classifier("cfg/coco.data", "cfg/yolov3.cfg", "/opt/weights/yolov3.weights", root="/tmp/darknet")

    def objects(self, file_path):
        return self.classifier.detect(file_path)

class IndexedMedia(object):
    def __init__(self, indexer, file_path):
        self.indexer=indexer
        self.file_path=file_path

    def __repr__(self):
        return

    @cached_property.cached_property
    def objects(self):
        return self.indexer.objects(self.file_path)
    @cached_property.cached_property
    def xxhash(self):
        return self.indexer.get_xxhash(self.file_path)
    @cached_property.cached_property
    def exif(self):
        return self.indexer.get_exif(self.file_path)
    @cached_property.cached_property
    def thumbnail(self):
        return self.indexer.get_thumbnail(self.file_path)
