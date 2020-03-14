#!/usr/bin/env python3
""" ."""
import json
import os

import get_files

import MediaIndexer.worker
from . import redis_cache
from . import redis_utils
from . import rq_utils
from .image_utils import to_pcts


def touch_sidecar(file_path):
    sidecar_path = f"{file_path}.json"
    if os.path.exists(sidecar_path):
        print(f"[X] sidecar: {file_path}")
        return
    else:
        print(f"[ ] sidecar: {file_path}")
        sidecar_data = {}
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


def cache_face_locations(file_path):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = redis_utils.load_databases(config_file)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_face_locations(**cfg)


def cache_face_encodings(file_path):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = redis_utils.load_databases(config_file)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_face_encodings(**cfg)


def cache_exif(file_path):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = redis_utils.load_databases(config_file)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_exif(**cfg)


def scan_dir(directory, worker_fcn="cache_xxhash"):
    """Scan a directory.

    1. Queue a scan of any found directories.
    2. Queue exif & thumbnail caching for any .jpeg files found.
    """
    config_file = os.environ.get("MEDIAINDEXER_CFG", "config.ini")
    queue_db = os.environ["MEDIAINDEXER_DB"]
    queue = rq_utils.get_queue(config_file=config_file, database=queue_db)

    for d in get_files.get_dirs(directory=directory, depth=1):
        if d.startswith("."):
            continue
        if ".zfs" in d:
            continue
        queue.enqueue(MediaIndexer.worker.scan_dir, d, worker_fcn)

    for image in get_files.get_files(
        directory=directory,
        extensions=[".jpg", ".jpeg", ".cr2", ".dng"],
        depth=1,
    ):
        fcn = getattr(MediaIndexer.worker, worker_fcn)
        queue.enqueue(fcn, image)
