"""MediaIndexer utilities module.

Generic utilities for use in MediaIndexer.
"""
import configparser
import io

from PIL import Image


def pil_thumbnail(thumbnail_str):
    assert isinstance(thumbnail_str, bytes)
    return Image.open(io.BytesIO(thumbnail_str))


def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


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


def to_pcts(image, face_locations):
    face_locations_pct = list()
    for face_location in face_locations:
        face_locations_pct.append(to_pct(image, face_location))
    return face_locations_pct
