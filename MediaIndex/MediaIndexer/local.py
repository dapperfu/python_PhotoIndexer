# -*- coding: utf-8 -*-
"""Functions for working with local files.

Functions for working with local files."""

import io

import exiftool
from PIL import Image
import pydarknet2
import xxhash


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


def get_thumbnail(file_path, size=size, pil_image=True):
    size = (size, size)
    if isinstance(file_path, bytes):
        file_path = file_path.decode("UTF-8")

    with open(file_path, "rb") as fp:
        img = Image.open(fp=fp)
        img.thumbnail(size)
        if pil_image:
            return img

        with io.BytesIO() as buffer:
            img.save(buffer, format="jpeg")
            thumbnail = buffer.getvalue()
        return thumbnail

def pil_thumbnail(thumbnail_str):
    assert isinstance(thumbnail_str, bytes)
    return Image.open(io.BytesIO(thumbnail_str))
