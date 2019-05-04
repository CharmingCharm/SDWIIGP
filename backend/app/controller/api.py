from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_required
from app.model import serialize
import json

from app.extension import db

api = Blueprint('api', __name__)

@api.route('/get_user', methods = ['GET', 'POST'])
def get_user():
    return json.dumps(serialize(current_user))
