#!/usr/bin/env python3
""" ."""
import json
import os

import face_recognition
import get_files
import MediaIndexer.worker

from . import redis_cache
from . import redis_utils
from . import rq_utils
from .utils import to_pcts


def populate_sidecar(image_path):
    sidecar_path = f"{image_path}.json"
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    sidecar_data = {
        "image_size": image.shape,
        "face_locations": face_locations,
        "face_locations_pct": to_pcts(image, face_locations),
        "xxhash": cache_xxhash(image_path),
        "exif": cache_exif(image_path),
    }
    with open(sidecar_path, "w") as fid:
        json.dump(sidecar_data, fid)


def cache_xxhash(file_path):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = redis_utils.load_databases(config_file)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_xxhash(**cfg)


def cache_exif(file_path):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = redis_utils.load_databases(config_file)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_exif(**cfg)


def cache_thumbnail(file_path, size):
    raise exc
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = redis_utils.load_databases(config_file)
    cfg = {
        "file_path": file_path,
        "size": size,
        "databases": databases,
    }
    redis_cache._get_thumbnail(**cfg)


def export_thumbnail(xxhash, export_dir="/tmp", size=128):
    for key in db.keys():
        tn_ = db.get(key)
        out = os.path.join("cache", size, f"{key.decode()}.jpg")
        MediaIndexer.utils.pil_thumbnail(tn_).save(out)


def scan_dir(directory):
    """Scan a directory.

    1. Queue a scan of any found directories.
    2. Queue exif & thumbnail caching for any .jpeg files found.
    """
    config_file = os.environ.get("MEDIAINDEXER_CFG", "config.ini")
    queue = rq_utils.get_queue(config_file=config_file, database="rq")

    for d in get_files.get_dirs(directory=directory, depth=1):
        if d.startswith("."):
            continue
        if ".zfs" in d:
            continue
        queue.enqueue(MediaIndexer.worker.scan_dir, d)

    for image in get_files.get_files(
        directory=directory, extensions=[".jpg", ".jpeg"], depth=1
    ):
        queue.enqueue(MediaIndexer.worker.cache_exif, image)
        queue.enqueue(MediaIndexer.worker.populate_sidecar, image)
