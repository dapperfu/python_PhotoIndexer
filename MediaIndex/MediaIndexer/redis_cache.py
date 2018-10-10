#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""redis_db module ^ utils.

"""
import json

import MediaIndexer.local
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
        XXHASH = MediaIndexer.local.get_xxhash(file_path)
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
    """Return exif for a given file_hash.

    If the result is cached in redis, it returns the redis value.
    If the result is not cached in redis it uses exiftool to:
        1. Get the exif data.
        2. Cache the exif data.
        3. Return the exif data.
    """
    for key, value in kwargs.items():
        print("{}: {}".format(key, value))
    # exif data is cached in the exif database.
    db = databases["exif"]
    # If the file_hash exists in the database.
    if db.exists(file_hash):
        # Get the raw exif data.
        exif_ = db.get(file_hash)
        # Clean up the raw exif data.
        exif = json.loads(exif_.decode("UTF-8").replace("'", "\""))
        # Print a cache hit.
        print("[X] EXIF : {}".format(file_path))
    else:
        # U
        exif = MediaIndexer.local.get_exif(file_path)
        exif_ = json.dumps(exif)
        db.set(file_hash, exif_)
        print("[ ] EXIF: {}".format(file_path))
    # Return the exif data.
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
        thumb_ = utils.get_thumbnail(file_path, pil_image=False)
        db.set(file_hash, thumb_)
        print("[ ] thumb : {}".format(file_path))

    return thumb_


class RedisUtilsMixin(object):
    """Mixin to do some housekeeping on Redis.

    Useful for development.
    """
    def flush_keys(self):
        """Flush all keys."""
        databases = self.databases
        for db_name, db in databases.items():
            print("{} db: flushing".format(db_name))

    def key_count(self):
        """Count Keys."""
        databases = self.databases
        for db_name, db in databases.items():
            print("{} db: {} keys".format(db_name, db.dbsize()))

class RedisCacheMixin(RedisUtilsMixin):
    """Mixin to cache results with Redis.

    """
    def get_xxhash(self, file_path):
        """Return the xxhash of a given media file.

        Cache if it is not already cached."""
        return _get_xxhash(file_path=file_path, databases=self.databases)

    def get_exif(self, file_path):
        """Return the EXIF of a given media file."""
        return _get_exif(file_path=file_path, databases=self.databases)


    def get_thumbnail(self, file_path):
        """Return a thumbnail of a given image file."""
        return _get_thumbnail(file_path=file_path, databases=self.databases)
