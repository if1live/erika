#-*- coding: utf-8 -*-

import flask

blueprint = flask.Blueprint('common', __name__, url_prefix='/common',
                            template_folder='templates')

@blueprint.route('/test')
def index():
    return 'ffs'

