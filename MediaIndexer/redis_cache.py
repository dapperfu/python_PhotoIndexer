#!/usr/bin/env python3
"""redis_db module ^ utils.

"""
import functools
import json
import os

from . import local


def _get_xxhash(file_path, databases, **kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
    if isinstance(file_path, bytes):
        file_path = file_path.decode("UTF-8")
    file_path = str(file_path)

    db = databases["cache_xxhash"]
    if db.exists(file_path):
        XXHASH = db.get(file_path).decode("UTF-8")
        print(f"[X] hash : {file_path}")
    else:
        XXHASH = local.get_xxhash(file_path)
        db.set(file_path, XXHASH)
        print(f"[ ] hash: {file_path}")

    db2 = databases["cache_xxhash_"]
    db2.append(XXHASH, os.pathsep)
    db2.append(XXHASH, file_path)
    return XXHASH


def hashop(f):
    """Operate on the hash of a file instead of the file path itself."""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if "file_hash" not in kwargs:
            file_hash = _get_xxhash(**kwargs)
            kwargs["file_hash"] = file_hash

        return f(*args, **kwargs)

    return wrapper


@hashop
def _get_exif(file_path, file_hash, databases, **kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

    db = databases["cache_exif"]
    if db.exists(file_hash):
        exif_ = db.get(file_hash)
        exif = json.loads(exif_.decode("UTF-8").replace("'", '"'))
        print(f"[X] EXIF : {file_path}")
    else:
        exif = local.get_exif(file_path)
        exif_ = json.dumps(exif)
        db.set(file_hash, exif_)
        print(f"[ ] EXIF: {file_path}")

    return exif


@hashop
def _get_thumbnail(file_path, file_hash, databases, size=128, **kwargs):
    for key, value in kwargs.items():
        print(f"* {key}: {value}")

    db_name = "cache_image_{size}x{size}".format(size=size)
    assert db_name in databases, db_name
    db = databases[db_name]
    if db.exists(file_hash):
        thumb_ = db.get(file_hash)
        print(f"[X] thumb({size}) : {file_path}")
    else:
        thumb_ = local.get_thumbnail(file_path, size=size, pil_image=False)
        db.set(file_hash, thumb_)
        print(f"[ ] thumb({size}) : {file_path}")

    return thumb_


class RedisCacheMixin:
    def get_xxhash(self, file_path):
        """Return the xxhash of a given media file.

        Cache if it is not already cached."""
        return _get_xxhash(file_path=file_path, databases=self.databases)

    def get_exif(self, file_path):
        return _get_exif(file_path=file_path, databases=self.databases)

    def get_thumbnail(self, file_path, size=128, pil_image=True):
        thumbnail_ = _get_thumbnail(
            file_path=file_path,
            databases=self.databases,
            size=size,
            pil_image=pil_image,
        )
        if pil_image:
            thumbnail = local.pil_thumbnail(thumbnail_)
        else:
            thumbnail = thumbnail_
        return thumbnail

    def cache_xxhash(self, file_path):
        self.get_xxhash(file_path)
        return None

    def cache_exif(self, file_path):
        self.get_xxhash(file_path)
        return None

    def cache_thumbnail(self, file_path):
        self.get_thumbnail(file_path)
        return None


class CacherMixin:
    pass
