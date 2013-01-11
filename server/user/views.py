#-*- coding: utf-8 -*-

import flask
blueprint = flask.Blueprint('user', __name__, url_prefix='/user',
                            template_folder='templates')

from flask import (
    render_template
    )

@blueprint.route('/')
def index():
    return render_template('common/base.html')
