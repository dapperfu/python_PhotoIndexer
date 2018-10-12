import io
import json
import os

import flask
from flask import (Blueprint, current_app, Flask, g, make_response,
                   render_template, request, send_file)
from flask_bootstrap import Bootstrap
from flask_restful import Api, reqparse, Resource
from werkzeug import HTTP_STATUS_CODES
import werkzeug.exceptions

import MediaIndexer
import MediaIndexer.redis_utils
from MediaIndexer.blueprints.gallery import gallery

parser = reqparse.RequestParser()
parser.add_argument("path")

api = Api()

admin = Blueprint('admin', __name__, url_prefix='/admin')
@admin.route('/')
def index():
    return "Hello Admin"


@gallery.route('/')
def gallery_base():
    return "Hello Admin"

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
        config_file = current_app.config["CONFIG"]
        indexer = MediaIndexer.MediaIndexer(config_file=config_file)

        args = parser.parse_args()
        args["xxhash"] = indexer.get_xxhash(args["path"])
        return args

class exif(Resource):
    def get(self):
        config_file = current_app.config["CONFIG"]
        indexer = MediaIndexer.MediaIndexer(config_file=config_file)

        args = parser.parse_args()
        args["exif"] = indexer.get_exif(args["path"])
        return args

for method in ["delete", "put", "post"]:
    setattr(xxhash, method, debug)
    setattr(exif, method, debug)

api_bp=Blueprint('api', __name__, url_prefix='/api')


api_cfg= {
    "app": api_bp,
    "prefix": "",
    "default_mediatype": 'application/json',
    "decorators": None,
    "catch_all_404s": False,
    "serve_challenge_on_401": False,
    "url_part_order": 'bae',
    "errors": None,
}
api = Api(**api_cfg)
api.add_resource(xxhash, "/xxhash")
api.add_resource(exif, "/exif")



base = Blueprint('base', __name__, url_prefix='/')
@base.route("/")
def blank():
    return "[This space intentionally left blank]"

@base.route("/thumbnails")
def thumbnails():
    path = request.args.get("path")

    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = MediaIndexer.redis_utils.load_databases(config_file)
    thumbnail = MediaIndexer.redis_cache._get_thumbnail(
        file_path=path, file_hash=None, databases=databases
    )
    return send_file(io.BytesIO(thumbnail), mimetype="image/jpg")

@base.route("/thumbnails/<string:xxhash>.jpg")
def thumbnails2(xxhash):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = MediaIndexer.redis_utils.load_databases(config_file)

    thumbnail = MediaIndexer.redis_cache._get_thumbnail(
        file_path="", file_hash=xxhash, databases=databases
    )
    return send_file(io.BytesIO(thumbnail), mimetype="image/jpg")

@base.route("/exif/<string:xxhash>.json")
def exif2(xxhash):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = MediaIndexer.redis_utils.load_databases(config_file)

    exif = MediaIndexer.redis_cache._get_exif(
        file_path="", file_hash=xxhash, databases=databases
    )
    return json.dumps(exif)

def create_app():
    app = flask.Flask(__name__, static_url_path="/static")
    app.config["DEBUG"] = True
    # Disable CSRF checking in WTForms
    app.config["WTF_CSRF_ENABLED"] = False
    # This is still necessary for SocketIO
    app.config["SECRET_KEY"] = os.urandom(12).hex()
    return app

def update_blueprints(app):
    app.register_blueprint(admin)
    app.register_blueprint(base)
    app.register_blueprint(api_bp)
    return app
