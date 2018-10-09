# -*- coding: utf-8 -*-
"""MediaIndexer utilities module.

Generic utilities for use in MediaIndexer.
"""

import io

import exiftool
from PIL import Image
import xxhash
import pydarknet2
classifier = pydarknet2.Classifier("cfg/coco.data", "cfg/yolov3.cfg", "/opt/weights/yolov3.weights", root="/tmp/darknet")


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
