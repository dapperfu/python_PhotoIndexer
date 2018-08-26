import configparser
import io
import os

from PIL import Image

from pony import orm
import redis
import rq
import utils

cfg_dir = os.path.dirname(os.path.abspath(__file__))
cfg = os.path.join(cfg_dir, "config.ini")

config = configparser.ConfigParser()
config.read(cfg)

exif_cache = redis.StrictRedis(
    host=config["redis"]["host"],
    port=config["redis"]["port"],
    db=config["redis"]["exif"],
)
xxhash_cache = redis.StrictRedis(
    host=config["redis"]["host"],
    port=config["redis"]["port"],
    db=config["redis"]["xxhash"],
)

thumb_cache = redis.StrictRedis(
    host=config["redis"]["host"],
    port=config["redis"]["port"],
    db=config["redis"]["thumb"],
)

rq_thumb = redis.StrictRedis(
    host=config["redis"]["host"],
    port=config["redis"]["port"],
    db=config["redis"]["rq_thumb"],
)

db = orm.Database()
provider = "mysql"
db.bind(
    provider=provider,
    host=config[provider]["host"],
    user=config[provider]["user"],
    passwd=config[provider]["pass"],
    db="media_index4",
)


class Thumbnail(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    xxhash = orm.Required(str, unique=True)
    thumbnail = orm.Optional(bytes)


db.generate_mapping()


def get_thumbnail(img_path, size=(255, 255)):
    if isinstance(img_path, bytes):
        img_path = img_path.decode("UTF-8")

    img = Image.open(img_path)
    img.thumbnail(size)
    with io.BytesIO() as buffer:
        img.save(buffer, format="jpeg")
        thumbnail = buffer.getvalue()
    return thumbnail


def cache_thumbnail(img_path, size=(255, 255)):
    if isinstance(img_path, bytes):
        img_path = img_path.decode("UTF-8")
    xxhash = utils.cache_xxhash(img_path)
    if Thumbnail.exists(xxhash=xxhash):
        return None

    thumbnail = get_thumbnail(img_path=img_path, size=size)

    Thumbnail(xxhash=xxhash, thumbnail=thumbnail)
    db.commit()
    return True


def cache_thumbnail_redis(img_path, size=(255, 255)):
    if isinstance(img_path, bytes):
        img_path = img_path.decode("UTF-8")

    xxhash = utils.cache_xxhash(img_path)

    if thumbnail_cache.exists(xxhash):
        # Do nothing, thumbnail cache already exists.
        return None

    thumbnail = get_thumbnail(img_path=img_path, size=size)
    return thumbnail_cache.set(xxhash, thumbnail)


if __name__ == "__main__":
    w = rq.Worker("default", connection=r)
    w.work()
