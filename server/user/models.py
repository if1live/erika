#-*- coding: utf-8 -*-

from flask.ext.login import (
    UserMixin,
    LoginManager,
)
from common import db
from settings import DB_PREFIX as prefix
from user import Anonymous

class UserOAuth(db.Model):
    __tablename__ = prefix + 'user_oauth'
    __table_args__ = (
        db.UniqueConstraint('provider', 'provider_uid'),
        )

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, 
                        db.ForeignKey(prefix + 'user.id',
                                      ondelete='CASCADE'))
    user = db.relationship('User')

    provider = db.Column(db.String(15))
    provider_uid = db.Column(db.String(31))
    token = db.Column(db.String(255))

    # auth 요청후 얻은 정보를 통째로 저장하기
    resp = db.Column(db.JSONEncodedDict)

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    def __init__(self, provider='', provider_uid='', oauth_token='', resp=None):
        self.provider = provider
        self.provider_uid = provider_uid
        self.token = oauth_token
        
        if resp is None:
            resp = {}
        self.resp = resp
    

class User(UserMixin, db.Model):
    __tablename__ = prefix + 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    is_admin = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __init__(self, name, email='', active=True, is_admin=False):
        self.name = name
        self.email = email
        self.active = active
        self.is_admin = is_admin

    def is_active(self):
        return self.active





