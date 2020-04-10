def redis_to_sidecar(file_path):
    sidecar_path = f"{file_path}.json"
    if os.path.exists(sidecar_path):
        with open(sidecar_path) as fp:
            sidecar_data = json.load(fp)
    else:
        sidecar_data = {}
    sidecar_data = {
        "image_size": image.shape,
        "face_locations": face_locations,
        "face_locations_pct": to_pcts(image, face_locations),
        "face_encodings": 
        "xxhash": cache_xxhash(file_path),
        "exif": cache_exif(file_path),
    }
    with open(sidecar_path, "w") as fp:
        json.dump(sidecar_data, fp)
