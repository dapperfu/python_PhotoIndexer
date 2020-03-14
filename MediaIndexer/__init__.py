import json
import os

import cached_property

from ._version import get_versions
from .redis_cache import RedisCacheMixin
from .redis_utils import load_databases
from .utils import read_config

__version__ = get_versions()["version"]
del get_versions


class MediaIndexer(RedisCacheMixin):
    def __init__(self, config_file):
        self.config_file = config_file

    @cached_property.cached_property
    def config(self):
        return read_config(self.config_file)

    @cached_property.cached_property
    def databases(self):
        return load_databases(self.config_file)

    def __repr__(self):
        return "MediaIndexer<{}>".format(os.path.basename(self.config_file))


class IndexedMedia:
    def __init__(self, indexer, file_path):
        self.indexer = indexer
        self.file_path = os.path.abspath(file_path)

    def __repr__(self):
        return f"IndexedMedia<{self.xxhash}>"

    @property
    def sidecar_file(self):
        return f"{self.file_path}.json"

    @property
    def sidecar(self):
        with open(self.sidecar_file) as fp:
            return json.load(fp)

    @sidecar.setter
    def sidecar(self, sidecar_data):
        with open(self.sidecar_file) as fp:
            json.dump(sidecar_data, fp)

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
