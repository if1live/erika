#-*- coding: utf-8 -*-

from flask.ext.login import (
    AnonymousUser,
    UserMixin,
    LoginManager,
)
from main import login_manager
from common import db

import datetime

PROVIDER_TWITTER = 'twitter'
PROVIDER_GITHUB = 'github'

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255))
    active = db.Column(db.Boolean)

    provider = db.Column(db.String(15))
    token = db.Column(db.String(255))
    provider_userid = db.Column(db.String(15))

    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    github_user_info = db.Column(db.JSONEncodedDict)

    def __init__(self, name, email='', active=True):
        self.name = name
        self.email = email
        self.active = active

    def is_active(self):
        return self.active

    @classmethod
    def get_oauth_user(cls, provider, user_code):
        user_code = unicode(user_code)
        q = db.session.query(cls).filter(
            cls.provider==provider, cls.provider_userid==user_code
            )
        return q.first()


class Anonymous(AnonymousUser):
    name = u'Anonymous'

login_manager.anonymous_user = Anonymous



class ConfigFile(db.Model):
    __tablename__ = 'configfile'

    id = db.Column(db.Integer, primary_key=True)
    filetype = db.Column(db.String(63))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=[user_id])

    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parent = db.relationship('User', foreign_keys=[parent_id])
    
    content = db.Column(db.String)
    desc = db.Column(db.String)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, filetype, user, content, desc):
        self.filetype = filetype
        self.user = user
        self.content = content
        self.desc = desc


class ConfigArchive(db.Model):
    __tablename__ = 'configarchive'

    id = db.Column(db.Integer, primary_key=True)
    filetype = db.Column(db.String(63))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')

    content = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, config_file):
        self.filetype = config_file.filetype
        self.user = config_file.user
        self.content = config_file.content

    
