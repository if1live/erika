#-*- coding: utf-8 -*-

from common.controllers import *
from .models import *
from common import db

def validate_filetype(filetype):
    '''
    .vimrc, .emacs, .bashrc 등등의 파일의 이름을 있는 그대로 쓰기 위한 목적이다
    영어 + 숫자 + (_, -, .) 으로 구성된 파일명 + 64글자 이하만 허용한다
    이를 벗어나는 경우는 설정파일의 이름이 아닐 가능성이 높다.
    '''
    import re
    MAX_LENGTH = 64
    if len(filetype) > MAX_LENGTH:
        return False
    
    regex = r'^[a-zA-Z-_.]+$'
    if re.match(regex, filetype) is None:
        return False
    else:
        return True


class ConfigFileController(BaseController):
    @classmethod 
    def get_config_list(cls, user_obj):
        q = db.session.query(cls.M).filter(
            cls.M.user==user_obj
            )
        return q.all()

    @classmethod
    def get_config(cls, user_obj, filetype):
        if validate_filetype(filetype) is False:
            raise ValueError('%s / %s is NOT valid file type' % (user_obj.name, filetype))


        q = db.session.query(cls.M).filter(
            cls.M.user==user_obj,
            cls.M.filetype==filetype
            )
        return q.first()

class ConfigArchiveController(BaseController):
    pass

register_controller(ConfigFile, ConfigFileController)
register_controller(ConfigArchive, ConfigArchiveController)
