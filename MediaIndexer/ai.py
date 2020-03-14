#!/usr/bin/env python3
"""
Machine Learning and Artificial Intelligence Module
"""
import face_recognition
import numpy as np
import pydarknet2
from PIL import Image

from .image_utils import load_image
from .image_utils import load_image_array


def get_face_locations(obj):
    """ Get the face locations given a file path."""
    if isinstance(obj, str):
        image = load_image_array(obj)
    elif isinstance(obj, Image):
        image = np.asarray(obj)
    elif isinstance(np.array):
        image = obj
    else:
        raise Exception(type(obj))
    face_locations = face_recognition.face_locations(image)

    return face_locations


def get_face_encodings(file_path, known_face_locations=None, aslist=False):
    """ Get the face locations given a file path."""
    if isinstance(file_path, str):
        image = load_image_array(file_path)
    elif isinstance(file_path, Image):
        image = np.asarray(file_path)
    elif isinstance(np.array):
        image = file_path
    else:
        raise Exception(type(file_path))

    face_encodings = face_recognition.face_encodings(
        image, known_face_locations=known_face_locations, num_jitters=1, model="small"
    )
    if aslist:
        return [list(encoding) for encoding in face_encodings]
    else:
        return face_encodings


def get_yolo3_objects(file_path):
    pass
