
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

import os
import cached_property
from .redis_db import load_databases
from .redis_cache import RedisCacheMixin, CacherMixin
import pydarknet2

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


    @cached_property.cached_property
    def classifier(self):
        return pydarknet2.Classifier("cfg/coco.data", "cfg/yolov3.cfg", "/opt/weights/yolov3.weights", root="/tmp/darknet")

    def objects(self, file_path):
        return self.classifier.detect(file_path)

class IndexedMedia(object):
    def __init__(self, indexer, file_path):
        self.indexer=indexer
        self.file_path=file_path


