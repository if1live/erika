#-*- coding: utf-8 -*-
from flask.ext.login import LoginManager, AnonymousUser


class Anonymous(AnonymousUser):
    name = u'Anonymous'
    is_admin = False

def init_login(app):
    login_manager = LoginManager()

    login_manager.login_view = "user.login"
    login_manager.logout_view = 'user.logout'
    login_manager.login_message = u"Please log in to access this page."
    login_manager.refresh_view = "user.reauth"
    login_manager.anonymous_user = Anonymous

    login_manager.setup_app(app)
    
    
    @login_manager.user_loader
    def load_user(id):
        from user.models import User
        from common import db
        return db.session.query(User).filter(User.id==id).first()

