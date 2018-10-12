from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import json

gallery = Blueprint('gallery', __name__, url_prefix='/g', template_folder='templates')

@gallery.route('/', defaults={'page': 'index'})
@gallery.route('/<page>')
def show(**kwargs):
    try:
        for key, item in kwargs.items():
            print("{}: {}".format(key, item))
        return json.dumps(kwargs)
    except TemplateNotFound:
        abort(404)


