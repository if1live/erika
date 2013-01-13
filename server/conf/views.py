#-*- coding: utf-8 -*-

import flask
blueprint = flask.Blueprint('conf', __name__, url_prefix='/conf',
                            template_folder='templates')

from flask import (
    render_template, request, redirect, url_for,
    )
from .models import *
from .controllers import *
from user.controllers import *

@blueprint.route('/view/<username>')
@blueprint.errorhandler(404)
def config_list(username):
    try:
        user_obj = UserController.get_user(username)
    except Exception as e:
        return e.message, 404

    conf_list = ConfigFileController.get_config_list(user_obj)
    raise RuntimeError
    return conf_list

@blueprint.route('/view/<username>/<filetype>')
@blueprint.errorhandler(404)
def view_config(username, filetype):
    try:
        user_obj = UserController.get_user(username)

        config = ConfigFileController.get_config(user_obj, filetype)
        if config is None:
            return '%s / %s is NOT exist' % (username, filetype), 404

    except Exception as e:
        return e.message, 404

@blueprint.route('/create/<username>/<filetype>', methods=['GET', 'POST',])
@blueprint.errorhandler(404)
def create_config(username, filetype):
    try:
        user_obj = UserController.get_user(username)

        if validate_filetype(filetype) is False:
            raise ValueError('%s / %s is NOT valid file type' % (username, filetype))
    
        return render_template('conf/create.html')
        #return username + filetype

    except Exception as e:
        return e.message, 404



