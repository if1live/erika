#-*- coding: utf-8 -*-

from flask.ext.login import (
    AnonymousUser,
    UserMixin,
)

from common import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    

    def __init__(self, name, id, active=True):
        pass
    
