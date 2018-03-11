import redis
import rq
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

r = redis.StrictRedis(
    host=config["redis"]["host"],
    port=config["redis"]["port"],
    db=config["redis"]["rq"],
)

w = rq.Worker("default", connection=r)
w.work()