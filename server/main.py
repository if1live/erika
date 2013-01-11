#-*- coding: utf-8 -*-

from flask import Flask
import settings

from flask import Flask, request, render_template, redirect, url_for, flash
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return self.active


class Anonymous(AnonymousUser):
    name = u"Anonymous"


USERS = {
    1: User(u"Notch", 1),
    2: User(u"Steve", 2),
    3: User(u"Creeper", 3, False),
}

USER_NAMES = dict((u.name, u) for u in USERS.itervalues())


app = Flask(__name__)
app.debug = settings.DEBUG
app.secret_key = settings.APP_SECRET_KEY


login_manager = LoginManager()

login_manager.anonymous_user = Anonymous
login_manager.login_view = "user.login"
login_manager.logout_view = 'user.logout'
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "user.reauth"

@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))

login_manager.setup_app(app)


if __name__ == "__main__":
    # set view
    def init_view(app):
        import common.views
        import user.views
        
        app.register_blueprint(common.views.blueprint)
        app.register_blueprint(user.views.blueprint)

    def init_db():
        from common import db

        import user.models

        db.Model.metadata.create_all(db.engine)

    init_view(app)
    init_db()

    app.run(host='0.0.0.0', port=8000)


