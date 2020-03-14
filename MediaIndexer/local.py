"""Functions for working with local files.

Functions for working with local files."""
import io
import os

import exiftool
import face_recognition
import pydarknet2
import rawpy
import xxhash
from PIL import Image

from .image import load_image


def get_xxhash(file_path):
    """ Get the xxhash of a given file."""
    hash64 = xxhash.xxh64()
    with open(str(file_path), "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash64.update(chunk)
    return hash64.hexdigest()


def get_exif(file_path):
    """ Get the exif of a given file."""
    with exiftool.ExifTool() as et:
        return et.get_metadata(str(file_path))
