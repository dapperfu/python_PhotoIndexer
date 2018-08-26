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

r = redis.StrictRedis(
    host=config["redis"]["host"],
    port=config["redis"]["port"],
    db=9,  # Thumbnail caching queue database
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


def cache_thumbnail(img_path, size=(255, 255)):
    xxhash = utils.cache_xxhash(img_path)
    img = Image.open(img_path)
    img.thumbnail(size)
    img
    with io.BytesIO() as buffer:
        img.save(buffer, format="jpeg")
        thumbnail = buffer.getvalue()
    try:
        Thumbnail(xxhash=xxhash, thumbnail=thumbnail)
        db.commit()
    except orm.CacheIndexError:
        pass
    except:
        raise


if __name__ == "__main__":
    w = rq.Worker("default", connection=r)
    w.work()
