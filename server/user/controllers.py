#-*- coding: utf-8 -*-

from common.controllers import BaseController, register_controller
from .models import *
from common import db

class UserController(BaseController):
    @classmethod
    def get_oauth_user(cls, provider, user_code):
        user_code = unicode(user_code)
        q = db.session.query(cls.M).filter(
            cls.M.provider==provider, cls.M.provider_userid==user_code
            )
        return q.first()

    @classmethod
    def get_github_user(cls, user_code):
        from user.models import PROVIDER_GITHUB
        return cls.get_oauth_user(PROVIDER_GITHUB, user_code)

    @classmethod
    def get_user(cls, username):
        user_obj = db.session.query(cls.M).filter(
            cls.M.name==username
            ).first()
        if user_obj is None:
            raise ValueError('User %s is NOT Exist' % username)
        else:
            return user_obj



register_controller(User, UserController)
