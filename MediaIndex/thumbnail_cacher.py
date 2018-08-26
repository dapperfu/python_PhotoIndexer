import configparser
import io
import os

from PIL import Image

from pony import orm
import rq

cfg_dir = os.path.dirname(os.path.abspath(__file__))
cfg = os.path.join(cfg_dir, "config.ini")

config = configparser.ConfigParser()
config.read(cfg)


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
