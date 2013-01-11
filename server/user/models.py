#-*- coding: utf-8 -*-

from flask.ext.login import (
    AnonymousUser,
    UserMixin,
    LoginManager,
)

from common import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    active = db.Column(db.Boolean)

    def __init__(self, id, name, email='', active=True):
        self.id = id
        self.name = name
        self.email = email
        self.active = active

    def is_active(self):
        return self.active

class Anonymous(AnonymousUser):
    name = u'Anonymous'


