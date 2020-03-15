"""image functions.
"""
import os

import rawpy
from PIL import Image


def load_image(file_path):
    """ Load image from the given path. """
    _, ext = os.path.splitext(file_path)
    if ext.lower() in [".dng", ".cr2"]:
        with rawpy.imread(file_path) as raw_:
            rgb = raw_.postprocess()
        img = Image.fromarray(rgb)
    else:
        with open(file_path, "rb") as fp:
            img = Image.open(fp=fp)
    return img


def str_to_pil(thumbnail_str):
    assert isinstance(thumbnail_str, bytes)
    return Image.open(io.BytesIO(thumbnail_str))


def cache_thumbnail(file_path, size):
    raise Exception("Bad idea")
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = redis_utils.load_databases(config_file)
    cfg = {"file_path": file_path, "size": size, "databases": databases}
    redis_cache._get_thumbnail(**cfg)


def export_thumbnail(xxhash, export_dir="/tmp", size=128):
    for key in db.keys():
        tn_ = db.get(key)
        out = os.path.join("cache", size, f"{key.decode()}.jpg")
        MediaIndexer.utils.pil_thumbnail(tn_).save(out)


def get_thumbnail(file_path, size, pil_image=True):

    size = (size, size)
    if isinstance(file_path, bytes):
        file_path = file_path.decode("UTF-8")

    ext = os.path.splitext(file_path)[1]

    with open(file_path, "rb") as fp:
        if ext.lower() in [".dng", ".cr2"]:
            with rawpy.imread(file_path) as raw_:
                rgb = raw_.postprocess()
            img = Image.fromarray(rgb)
        else:
            img = Image.open(fp=fp)
        img.thumbnail(size)
        if pil_image:
            return img

        with io.BytesIO() as buffer:
            img.save(buffer, format="jpeg")
            thumbnail = buffer.getvalue()
        return thumbnail


def pil_thumbnail(thumbnail_str):
    assert isinstance(thumbnail_str, bytes)
    return Image.open(io.BytesIO(thumbnail_str))
