from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import json

gallery = Blueprint('gallery', __name__, template_folder='templates', url_prefix='/g')

@gallery.route('/', defaults={'page': 'index'})
@gallery.route('/<page>')
def index(**kwargs):
    for key, item in kwargs.items():
        print("{}: {}".format(key, item))
    return json.dumps(kwargs)
