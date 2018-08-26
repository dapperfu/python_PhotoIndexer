import io

import exiftool
from PIL import Image
import xxhash


def get_xxhash(fname):
    """ Get the xxhash of a given file."""
    hash64 = xxhash.xxh64()
    with open(str(fname), "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash64.update(chunk)
    return hash64.hexdigest()


def get_exif(fname):
    """Get the exif of a given file."""
    with exiftool.ExifTool() as et:
        return et.get_metadata(str(fname))


def get_thumbnail(img_path, size=(255, 255)):
    if isinstance(img_path, bytes):
        img_path = img_path.decode("UTF-8")

    img = Image.open(img_path)
    img.thumbnail(size)
    with io.BytesIO() as buffer:
        img.save(buffer, format="jpeg")
        thumbnail = buffer.getvalue()
    return thumbnail


def pil_thumbnail(thumbnail_str):
    assert isinstance(thumbnail_str, bytes)
    return Image.open(io.BytesIO(thumbnail_str))
