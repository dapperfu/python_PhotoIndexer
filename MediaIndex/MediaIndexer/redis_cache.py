#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""redis_db module ^ utils.

"""
import json

from . import local
import cached_property

import functools

def _get_xxhash(file_path, databases):
    if isinstance(file_path, bytes):
        file_path = file_path.decode("UTF-8")
    file_path = str(file_path)

    db = databases["xxhash"]
    if db.exists(file_path):
        XXHASH = db.get(file_path).decode("UTF-8")
        print("[X] hash : {}".format(file_path))
    else:
        XXHASH = local.get_xxhash(file_path)
        db.set(file_path, XXHASH)
        print("[ ] hash: {}".format(file_path))
    return XXHASH

def hashop(f):
    """Operate on the hash of a file instead of the file path itself."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        file_hash = _get_xxhash(**kwargs)
        kwargs["file_hash"] = file_hash

        return f(*args, **kwargs)
    return wrapper

@hashop
def _get_exif(file_path, file_hash, databases, **kwargs):
    for key, value in kwargs.items():
        print("{}: {}".format(key, value))

    db = databases["exif"]
    if db.exists(file_hash):
        exif_ = db.get(file_hash)
        exif = json.loads(exif_.decode("UTF-8").replace("'", "\""))
        print("[X] EXIF : {}".format(file_path))
    else:
        exif = local.get_exif(file_path)
        exif_ = json.dumps(exif)
        db.set(file_hash, exif_)
        print("[ ] EXIF: {}".format(file_path))

    return exif

@hashop
def _get_thumbnail(file_path, file_hash, databases, **kwargs):
    for key, value in kwargs.items():
        print("{}: {}".format(key, value))

    db = databases["thumb"]
    if db.exists(file_hash):
        thumb_ = db.get(file_hash)
        print("[X] thumb : {}".format(file_path))
    else:
        thumb_ = local.get_thumbnail(file_path, pil_image=False)
        db.set(file_hash, thumb_)
        print("[ ] thumb : {}".format(file_path))

    return thumb_


class RedisCacheMixin(object):
    def get_xxhash(self, file_path):
        """Return the xxhash of a given media file.

        Cache if it is not already cached."""
        return _get_xxhash(file_path=file_path, databases=self.databases)


    def get_exif(self, file_path):
        return _get_exif(file_path=file_path, databases=self.databases)


    def get_thumbnail(self, file_path, pil_image=True):
        thumbnail = _get_thumbnail(file_path=file_path, databases=self.databases)

    def cache_xxhash(self, file_path):
        self.get_xxhash(file_path)
        return None


    def cache_exif(self, file_path):
        self.get_xxhash(file_path)
        return None

    def cache_thumbnail(self, file_path):
        self.get_thumbnail(file_path)
        return None

class CacherMixin(object):
    pass
