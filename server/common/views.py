#-*- coding: utf-8 -*-

import flask

blueprint = flask.Blueprint('common', __name__, url_prefix='/common',
                            template_folder='templates')

from flask import render_template

@blueprint.route('/test')
def index():
    return render_template('common/index.html')

