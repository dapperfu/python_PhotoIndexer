from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import json

thumbnail_blueprint = Blueprint('thumbnails', __name__, template_folder='templates', url_prefix='/admin')

@thumbnail_blueprint.route('/')
def index():
    return "Hello Thumbnails."
