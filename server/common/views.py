#-*- coding: utf-8 -*-

import flask

blueprint = flask.Blueprint('common', __name__, url_prefix='/common',
                            template_folder='templates')

from main import app
from flask import render_template, Response
from common import db
from sqlalchemy import distinct

@blueprint.route('/common.js')
def common_js():
    from conf.models import ConfigFile

    embed_filetype_list = [
        '.vimrc',
        '.emacs',
        '.tmux.conf',
        '.bashrc',
        ]

    exist_filetype_list = db.session.query(distinct(ConfigFile.filetype)).all()
    exist_filetype_list = map(lambda x: x[0], exist_filetype_list)

    filetype_list = embed_filetype_list + exist_filetype_list
    filetype_set = set(filetype_list)
    filetype_list = list(filetype_set)

    data = {
        'filetype_list' : filetype_list,
        }
    content = render_template('common/common.js', **data)
    return Response(response=content, mimetype="application/javascript")
