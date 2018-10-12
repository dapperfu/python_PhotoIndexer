from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import json

thumbnails = Blueprint('thumbnails', __name__, template_folder='templates', url_prefix='/thumbnails')

@thumbnails.route('/')
def get_thumbnail(xxhash):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = MediaIndexer.redis_utils.load_databases(config_file)

    thumbnail = MediaIndexer.redis_cache._get_thumbnail(
        file_path="", file_hash=xxhash, databases=databases
    )
    return send_file(io.BytesIO(thumbnail), mimetype="image/jpg")
