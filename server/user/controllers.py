#-*- coding: utf-8 -*-

from common.controllers import BaseController, register_controller
from .models import *


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


class ConfigFileController(BaseController):
    pass

class ConfigArchiveController(BaseController):
    pass

register_controller(User, UserController)
register_controller(ConfigFile, ConfigFileController)
register_controller(ConfigArchive, ConfigArchiveController)
