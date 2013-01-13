#-*- coding: utf-8 -*-

import flask

blueprint = flask.Blueprint('common', __name__, url_prefix='/',
                            template_folder='templates')

from flask import render_template

@blueprint.route('/')
def index():
    return render_template('common/index.html')

