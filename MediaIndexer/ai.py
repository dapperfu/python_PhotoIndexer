#!/usr/bin/env python3
"""
Created on Sat Mar 14 04:46:34 2020

@author: user1
"""
import face_recognition
import pydarknet2

from .image_utils import load_image
from .image_utils import to_pcts


def get_face_locations(file_path):
    image = load_image(file_path)
    image = face_recognition.load_image_file(file_path)
    face_locations = face_recognition.face_locations(image)

    return face_locations


def get_face_encodings(file_path, known_face_locations=None):
    image = load_image(file_path)
    face_encodings = face_recognition.face_encodings(
        image,
        known_face_locations=known_face_locations,
        num_jitters=1,
        model="small",
    )
    return face_encodings
    return [list(encoding) for encoding in face_encodings]


def get_yolo3_objects(file_path):
    pass
