import json
import os

import cached_property

from ._version import get_versions
from .redis_cache import RedisCacheMixin
from .redis_utils import load_databases
from .utils import read_config
from .image_utils import get_thumbnail
from .image_utils import load_image

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

class Face:
    def __init__(self, media, face_location, face_encoding):
        self.media = media
        self.face_location = face_location
        self.face_encoding = face_encoding
        
    def __repr__(self):
        return f"Face<{self.media.xxhash}, {self.face_location}>"

class IndexedMedia:
    def __init__(self, indexer, file_path):
        self.indexer = indexer
        self.file_path = os.path.abspath(file_path)

    def __repr__(self):
        return f"IndexedMedia<{self.xxhash}>"
        
    @cached_property.cached_property
    def img(self):
        return load_image(self.file_path)

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
    def face_locations(self):
        return self.indexer.get_face_locations(self.file_path)
        
    @cached_property.cached_property
    def face_encodings(self):
        return self.indexer.get_face_encodings(self.file_path)
        
    @property
    def faces(self):
        faces = list()
        for location, encoding in zip(self.face_locations, self.face_encodings):
            faces.append(Face(self, location, encoding))
        return faces
        

    @cached_property.cached_property
    def thumbnail(self):
        return get_thumbnail(self.file_path)
