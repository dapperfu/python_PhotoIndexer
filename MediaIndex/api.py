import io
import json
import os

from flask import Flask, make_response, request, send_file
from flask_bootstrap import Bootstrap
from flask_restful import Api, reqparse, Resource

import MediaIndexer
import MediaIndexer.redis_cache

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("path")


cfg = os.path.abspath("config_m6700.ini")
assert os.path.exists(cfg)

indexer = MediaIndexer.MediaIndexer(cfg)


def debug(self, *args, **kwargs):
    args = parser.parse_args()
    print(args)
    for i, arg in enumerate(args):
        print("{}: {}".format(i, arg))

    for key, value in kwargs.items():
        print("{}: {}".format(key, value))
    return args


class xxhash(Resource):
    def get(self):
        args = parser.parse_args()
        args["xxhash"] = indexer.get_xxhash(args["path"])
        return args


class exif(Resource):
    def get(self):
        args = parser.parse_args()
        args["exif"] = indexer.get_exif(args["path"])
        return args


for method in ["delete", "put", "post"]:
    setattr(xxhash, method, debug)
    setattr(exif, method, debug)

api.add_resource(xxhash, "/api/xxhash")
api.add_resource(exif, "/api/exif")


@app.route("/thumbnails")
def thumbnails():
    path = request.args.get("path")

    thumbnail = indexer.get_thumbnail(path, pil_image=False)

    return send_file(io.BytesIO(thumbnail), mimetype="image/jpg")


@app.route("/thumbnails/<string:xxhash>.jpg")
def thumbnails2(xxhash):
    thumbnail = MediaIndexer.redis_cache._get_thumbnail(
        file_path="", file_hash=xxhash, databases=indexer.databases
    )
    return send_file(io.BytesIO(thumbnail), mimetype="image/jpg")


@app.route("/exif/<string:xxhash>.json")
def exif2(xxhash):
    exif = MediaIndexer.redis_cache._get_exif(
        file_path="", file_hash=xxhash, databases=indexer.databases
    )
    return json.dumps(exif)


# <image src="data:image/png;base64,' + caffe.draw.draw_net(net, "UD").encode("base64") + '" style="max-width:100%" />
if __name__ == "__main__":
    app.run(debug=True)
