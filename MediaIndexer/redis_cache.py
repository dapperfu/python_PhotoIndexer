#!/usr/bin/env python3
"""redis_db module utils.

"""
import functools
import json
import os

from . import ai
from . import local
from .utils import arr_to_bytes
from .utils import bytes_to_arr


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
def _get_face_locations(file_path, file_hash, databases, **kwargs):
    sidecar_path = f"{file_path}.json"
    try:
        with open(sidecar_path) as fp:
            sidecar_data = json.load(fp)
    except:
        sidecar_data = dict()
    for key, value in kwargs.items():
        print(f"{key}: {value}")
    db = databases["cache_face_locations"]
    if db.exists(file_hash):
        face_locations_ = db.get(file_hash)
        face_locations = json.loads(
            face_locations_.decode("UTF-8").replace("'", '"')
        )
        print(f"[X] face_locations : {file_path}")
    elif "face_locations" in sidecar_data:
        face_locations = sidecar_data["face_locations"]
        print(f"[#] face_locations : {file_path}")
        face_locations_ = json.dumps(face_locations)
        db.set(file_hash, face_locations_)
    else:
        face_locations = ai.get_face_locations(file_path)
        face_locations_ = json.dumps(face_locations)
        db.set(file_hash, face_locations_)
        print(f"[ ] face_locations: {file_path}")

    return face_locations


@hashop
def _get_face_encodings(file_path, file_hash, databases, **kwargs):
    sidecar_path = f"{file_path}.json"
    try:
        with open(sidecar_path) as fp:
            sidecar_data = json.load(fp)
    except:
        sidecar_data = dict()
    for key, value in kwargs.items():
        print(f"{key}: {value}")
    db = databases["cache_face_encodings"]
    if db.exists(file_hash):
        face_encodings_ = db.get(file_hash)
        face_encodings = bytes_to_arr(face_encodings_)
        print(f"[X] face_encodings : {file_path}")
    elif "face_encodings" in sidecar_data:
        raise Exception("Not Yet.")
    else:
        face_locations = _get_face_locations(
            file_path=file_path, file_hash=file_hash, databases=databases
        )
        face_encodings = ai.get_face_encodings(
            file_path=file_path, known_face_locations=face_locations
        )
        face_encodings_ = arr_to_bytes(face_encodings)
        db.set(file_hash, face_encodings_)
        print(f"[ ] face_encodings: {file_path}")
    return face_encodings


class RedisCacheMixin:
    def get_xxhash(self, file_path):
        """Return the xxhash of a given media file.

        Cache if it is not already cached."""
        return _get_xxhash(file_path=file_path, databases=self.databases)

    def get_exif(self, file_path):
        return _get_exif(file_path=file_path, databases=self.databases)

    def get_face_locations(self, file_path):
        return _get_face_locations(
            file_path=file_path, databases=self.databases
        )

    def get_face_encodings(self, file_path):
        return _get_face_encodings(
            file_path=file_path, databases=self.databases
        )

    def cache_xxhash(self, file_path):
        self.get_xxhash(file_path)
        return None

    def cache_exif(self, file_path):
        self.get_xxhash(file_path)
        return None

    def cache_face_locations(self, file_path):
        self.get_face_locations(file_path)
        return None


class CacherMixin:
    pass
