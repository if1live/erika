#-*- coding: utf-8 -*-

from common.controllers import BaseController, register_controller
from .models import *
from common import db

class UserController(BaseController):
    @classmethod
    def is_valid_name(cls, nick):
        '''
        닉네임은 가입시에 pk에서 떙겨서 쓰는데 닉네임을 수동으로 숫자로 설정할 경우
        자동생성과 겹칠 가능성이 존재한다. 그래서 이를 방지하기 위해서
        숫자로만 구성된 닉네임은 금지한다.
        모든 숫자를 금지하는것은 아니고 0으로 시작하는 숫자는 허용한다.
        pk기반으로 땡겨고면 123은 자동생성될수 있지만 0123은 자동생성될리가 없으니까
        '''
        import re
        regex_str = r'^[1-9][0-9]*$'
        m = re.search(regex_str, nick)
        return m is None

    @classmethod
    def get_valid_name(cls, name):
        # 닉네임은 유저마다 고유하기떄문에 검색해보고 중복이 있으면
        # 뒤에 적절한 내용을 붙여준다
        if name == '':
            # 이름이 없는 경우는 자동생성하기가 영..그러니까 따로 처리
            return name

        base_name = name
        count = 0
        while True:
            q = db.session.query(cls.M).filter(cls.M.name==name)
            if q.count() == 0 and cls.is_valid_name(name) == True:
                return name
            count += 1
            name = '%s%d' % (base_name, count)

            if count >= 100:
                raise ValueError('unknown')

    @classmethod
    def get_user(cls, username):
        user_obj = db.session.query(cls.M).filter(
            cls.M.name==username
            ).first()
        if user_obj is None:
            raise ValueError('User %s is NOT Exist' % username)
        else:
            return user_obj

class UserOAuthController(BaseController):
    @classmethod
    def is_exist(cls, info):
        q = db.session.query(cls.M).filter(
            cls.M.provider == info.provider,
            cls.M.provider_uid == info.provider_uid,
            )
        return q.count() > 0

    @classmethod
    def get(cls, info):
        return db.session.query(cls.M).filter(
            cls.M.provider == info.provider,
            cls.M.provider_uid == info.provider_uid,
            ).first()

register_controller(UserOAuth, UserOAuthController)
register_controller(User, UserController)
