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
    data = {
        'conf_list': conf_list,
        'username': username
        }
    return render_template('conf/list.html', **data)

@blueprint.route('/view/<username>/<filetype>')
@blueprint.errorhandler(404)
def view_config(username, filetype):
    try:
        user_obj = UserController.get_user(username)

        config = ConfigFileController.get_config(user_obj, filetype)
        if config is None:
            return '%s / %s is NOT exist' % (username, filetype), 404

        data = {
            'filetype' : filetype,
            'conf' : config,
            }
        return render_template('conf/view.html', **data)

    except Exception as e:
        return e.message, 404

@blueprint.route('/create/<username>', methods=['GET', 'POST',])
@blueprint.errorhandler(404)
def create_config(username):
    try:
        user_obj = UserController.get_user(username)
    except Exception as e:
        return e.message, 404

    if request.method == 'GET':
        filetype = request.args.get('filetype')
        if validate_filetype(filetype) is False:
            return '%s / %s is NOT valid file type' % (username, filetype), 400

        # 이전에 등록된것이 있는지 찾아보고 있으면 일단 넣어준다
        config = ConfigFileController.get_config(user_obj, filetype)
        data = {
            'filetype' : filetype,
            'conf' : config,
            }
        return render_template('conf/create.html', **data)
    
    else:
        filetype = request.form['filetype']
        content = request.form['content']
        desc = request.form['desc']
        print filetype, content, desc
        
        ConfigFileController.save(user_obj, filetype, content, desc)
        
        return redirect('/conf/view/%s/%s' % (username, filetype))




