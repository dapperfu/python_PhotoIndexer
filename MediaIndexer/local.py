"""Functions for working with local files.

Functions for working with local files."""
import io
import os

import exiftool
import pydarknet2
import rawpy
import xxhash
from PIL import Image


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


def get_thumbnail(file_path, size, pil_image=True):

    size = (size, size)
    if isinstance(file_path, bytes):
        file_path = file_path.decode("UTF-8")

    ext = os.path.splitext(file_path)[1]

    with open(file_path, "rb") as fp:
        if ext.lower() in [".dng", ".cr2"]:
            with rawpy.imread(file_path) as raw_:
                rgb = raw_.postprocess()
            img = Image.fromarray(rgb)
        else:
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
