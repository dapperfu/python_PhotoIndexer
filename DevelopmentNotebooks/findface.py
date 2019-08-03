#!/usr/bin/env python
# coding: utf-8
import os
import sys
sys.path.append("/opt/opencv4/lib/python3.7/site-packages")
import cv2
import face_recognition
import get_files
from PIL import Image
import sys

def buffer_face(face_location, shape, bf=1):
    top, right, bottom, left = face_location
    h = bottom - top
    w = right - left
    h_ = h * bf
    w_ = w * bf
    return [
        int(max(top - h_, 0)),
        int(min(bottom + h_, shape[0])),
        int(max(left - w_, 0)),
        int(min(right + w_, shape[1])),
    ]
    
good_videos = get_files.get_files("/projects/2020/Stage_1")


face_folder_root = "/projects/2020/MeFaces"

def extract_videos(video_file):
    basename = os.path.splitext(os.path.basename(video_file))[0]
    face_folder = os.path.join(face_folder_root, basename)
    if os.path.exists(face_folder):
        print("... Whoop ...")
        sys.stdout.flush()
        return
    os.makedirs(face_folder, exist_ok=True)
    frames = []
    batch_size = 2
    video_capture = cv2.VideoCapture(video_file)
    
    for frame_count in range(int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))):
        print("#", end="")
        sys.stdout.flush()
        # Grab a single frame of video
        ret, frame = video_capture.read()
    
        # Bail out when the video file ends
        if not ret:
            continue
    
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which
        # face_recognition uses)
        frame = frame[:, :, ::-1]
    
        # Save each frame of the video to a list
        frames.append(frame)
        # Every 128 frames (the default batch size), batch process the list of
        # frames to find faces
        if len(frames) >= batch_size:
            print(":", end="")
            sys.stdout.flush()
            batch_of_face_locations = face_recognition.batch_face_locations(
                frames, number_of_times_to_upsample=0)
            for frame_number_in_batch, face_locations in enumerate(
                    batch_of_face_locations):
                print(".", end="")
                sys.stdout.flush()
                frame_number = frame_count - batch_size + frame_number_in_batch
                image = frames[frame_number_in_batch]
                for face_number, face_location in enumerate(face_locations):
                    print("!", end="");
                    sys.stdout.flush()

                    # Print the location of each face in this frame
                    top, bottom, left, right = buffer_face(face_location, image.shape, bf=0.75)
                    face_image = image[top:bottom, left:right]
                    pil_image = Image.fromarray(face_image)
                    face_file = "{}_{:06d}_{:02d}.png".format(
                        basename, frame_number, face_number)
                    pil_image.save(os.path.join(face_folder, face_file))
            frames = list()

for video_file in good_videos:
    print(video_file)
    sys.stdout.flush()
    extract_videos(video_file)
