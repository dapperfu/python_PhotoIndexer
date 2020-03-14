def cache_faces(file_path):
    sidecar_path = f"{file_path}.json"

    if os.path.exists(sidecar_path):
        with open(sidecar_path) as fp:
            sidecar_data = json.load(fp)
    else:
        sidecar_data = {}
    if "face_locations" in sidecar_data:
        print(f"[X] faces: {file_path}")
        return
    else:
        print(f"[ ] faces: {file_path}")
    image = face_recognition.load_image_file(file_path)
    face_locations = face_recognition.face_locations(image)
    sidecar_data = {
        "image_size": image.shape,
        "face_locations": face_locations,
        "face_locations_pct": to_pcts(image, face_locations),
        "xxhash": cache_xxhash(file_path),
        "exif": cache_exif(file_path),
    }
    with open(sidecar_path, "w") as fp:
        json.dump(sidecar_data, fp)
