"""image utils"""
import copy
import io
import os

import numpy as np
import rawpy
from PIL import Image


def load_image_array(file_path: str):
    """ Loads both jpg and raw image file formats. Returns rgb numpy array. """
    _, ext = os.path.splitext(file_path)
    if ext.lower() in [".dng", ".cr2"]:
        with rawpy.imread(file_path) as raw_:
            rgb = raw_.postprocess()
    else:
        img = Image.open(file_path)
        rgb = np.asarray(img)
    return rgb


def load_image(file_path: str):
    """ Loads both jpg and raw image file formats. Returns Image. """
    _, ext = os.path.splitext(file_path)
    if ext.lower() in [".dng", ".cr2"]:
        with rawpy.imread(file_path) as raw_:
            rgb = raw_.postprocess()
            img = copy.deepcopy(Image.fromarray(rgb))
    else:
        img = copy.deepcopy(Image.open(file_path))
    return img


def pil_to_bytes(image: Image) -> bytes:
    """ Convert a PIL Image into a byte string for redis & mysql. """
    with io.BytesIO() as buffer:
        image.save(buffer, format="jpeg")
        image_bytes = buffer.getvalue()
    return image_bytes


def bytes_to_pil(thumbnail_str: bytes) -> Image:
    """ Convert a byte string containing a jpeg into a PIL Image. """
    assert isinstance(thumbnail_str, bytes)
    return Image.open(io.BytesIO(thumbnail_str))


def get_thumbnail(file_path: str, size: int = 128):
    """ Return a thumbnail. """
    img = load_image(file_path)
    img.thumbnail((size, size))
    return img


def to_pct(image, face_location):
    top, right, bottom, left = face_location

    h, w, _ = image.shape

    top_pct = top / h
    bottom_pct = bottom / h
    left_pct = left / w
    right_pct = right / w
    return top_pct, right_pct, bottom_pct, left_pct


def from_pct(image, face_location_pct):
    top_pct, right_pct, bottom_pct, left_pct = face_location_pct
    h, w, _ = image.shape
    top = int(np.floor(top_pct * h))
    bottom = int(np.ceil(bottom_pct * h))
    left = int(np.floor(left_pct * w))
    right = int(np.ceil(right_pct * w))

    face_location = top, right, bottom, left
    return face_location


def from_pcts(image, face_locations_pct):
    face_locations = list()
    for face_location_pct in face_locations_pct:
        face_locations.append(from_pct(image, face_location_pct))
    return face_locations


def to_pcts(image, face_locations):
    face_locations_pct = list()
    for face_location in face_locations:
        face_locations_pct.append(to_pct(image, face_location))
    return face_locations_pct
