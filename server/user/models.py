#-*- coding: utf-8 -*-

from flask.ext.login import (
    AnonymousUser,
    UserMixin,
    LoginManager,
)
from main import login_manager
from common import db

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



