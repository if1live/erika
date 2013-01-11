#-*- coding: utf-8 -*-

from flask import Flask
import settings

app = Flask(__name__)
app.debug = settings.DEBUG
app.secret_key = settings.APP_SECRET_KEY

from flask.ext.login import LoginManager
#from user.models import Anonymous

login_manager = LoginManager()

login_manager.login_view = "user.login"
login_manager.logout_view = 'user.logout'
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "user.reauth"

login_manager.setup_app(app)

@login_manager.user_loader
def load_user(id):
    from user.models import User
    return User('asd')
    #return User.get(id)

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


