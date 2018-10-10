# -*- coding: utf-8 -*-
"""MediaIndexer utilities module.

Generic utilities for use in MediaIndexer.
"""

import io

import exiftool
from PIL import Image
import xxhash
import pydarknet2

def get_xxhash(file_path):
    """ Get the xxhash of a given file."""
    hash64 = xxhash.xxh64()
    with open(str(file_path), "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash64.update(chunk)
    return hash64.hexdigest()


def get_exif(file_path):
    """Get the exif of a given file."""
    with exiftool.ExifTool() as et:
        return et.get_metadata(str(file_path))


def get_thumbnail(file_path, size=(255, 255), pil_image=True):
    if isinstance(file_path, bytes):
        file_path = file_path.decode("UTF-8")

    img = Image.open(file_path)
    img.thumbnail(size)
    if pil_image:
        return img

    with io.BytesIO() as buffer:
        img.save(buffer, format="jpeg")
        thumbnail = buffer.getvalue()
    return thumbnail

def get_objects(file_path):
    """ Get objects in a given image."""
    if isinstance(file_path, bytes):
        file_path = file_path.decode("UTF-8")
    return classifier.detect(file_path)

def pil_thumbnail(thumbnail_str):
    assert isinstance(thumbnail_str, bytes)
    return Image.open(io.BytesIO(thumbnail_str))

@cached_property.cached_property
    def connection(self):
        return self.databases["rq"]

    @cached_property.cached_property
    def queue(self):
        return rq.Queue(connection=self.connection)

    def cache_dir(self, root_dir):
        # Scan for directories in the given root directory, to a depth of 1
        media_dirs = get_files.get_dirs(root_dir, depth=1)
        # For each found directory:
        for media_dir in media_dirs:
            # Don't scan zfs snap directories
            if ".zfs" in media_dir:
                continue
            # Don't follow symbolic links.
            if os.path.islink(media_dir):
                continue
            # Queue scanning the folder.
            self.queue.enqueue(cache_dir, media_dir)
        # Scan given directory for files, to a depth of 1
        media_files = get_files.get_files(root_dir, depth=1)
        # For each media_file:
        for media_file in media_files:
            # Queue scanning the media's exif data.
            self.queue.enqueue(self.cache_thumbnail, media_file)

def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config
