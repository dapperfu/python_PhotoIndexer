#!/usr/bin/env python3
import json
import os

import dlib
import face_recognition
import get_files
import numpy as np
from IPython.display import display
from IPython.display import display_jpeg
from PIL import Image


dlib.DLIB_USE_CUDA = True
import sys


def from_pct(image, face_location_pct):
    top_pct, right_pct, bottom_pct, left_pct = face_location_pct
    h, w, _ = image.shape
    top = int(np.floor(top_pct * h))
    bottom = int(np.ceil(bottom_pct * h))
    left = int(np.floor(left_pct * w))
    right = int(np.ceil(right_pct * w))

    face_location = top, right, bottom, left
    return face_location


def extract_faces(sidecar_path):
    print(".", end="")
    image_path = f"{os.path.splitext(sidecar_path)[0]}.jpg"
    with open(sidecar_path) as fid:
        sidecar_data = json.load(fid)
    if len(sidecar_data["face_locations_pct"]) == 0:
        return
    image = face_recognition.load_image_file(image_path)
    for img_idx, face_location_pct in enumerate(sidecar_data["face_locations_pct"]):
        print("$", end="")
        top, right, bottom, left = from_pct(image, face_location_pct)
        face_image = image[top:bottom, left:right]
        if face_image.size < 10000:
            print("%", end="")
            continue
        pil_image = Image.fromarray(face_image)
        if image_path.startswith("/projects/Camera"):
            face_path = image_path.replace("/projects/Camera", "/projects/Faces")
        elif image_path.startswith("/home/user1/Pictures"):
            face_path = image_path.replace("/home/user1/Pictures", "/projects/Faces2")
        elif image_path.startswith("/projects/Pictures"):
            face_path = image_path.replace("/projects/Pictures", "/projects/Faces3")
        else:
            raise Exception(image_path)
        base_path, ext = os.path.splitext(face_path)
        os.makedirs(os.path.dirname(face_path), exist_ok=True)
        pil_image.save(f"{base_path}+{img_idx:02d}{ext}")
    print("")


def to_pct(image, face_location):
    top, right, bottom, left = face_location

    h, w, _ = image.shape

    top_pct = top / h
    bottom_pct = bottom / h
    left_pct = left / w
    right_pct = right / w
    return top_pct, right_pct, bottom_pct, left_pct


def to_pcts(image, face_locations):
    face_locations_pct = list()
    for face_location in face_locations:
        face_locations_pct.append(to_pct(image, face_location))
    return face_locations_pct


def debug():
    print(f"CUDA Devices Found: {dlib.cuda.get_num_devices()}")
    print(sys.argv)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        debug()
        sys.exit()
    sidecars = get_files.get_files(sys.argv[1], extensions=".json")
    for idx, sidecar in enumerate(sidecars):
        extract_faces(sidecar)
sys.exit()
