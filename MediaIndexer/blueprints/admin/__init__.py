from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import json

admin = Blueprint('admin', __name__, template_folder='templates', url_prefix='/admin')

@admin.route('/')
def index():
    return "Hello Admin"
