#-*- coding: utf-8 -*-

from flask import Flask, render_template
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
    from common import db
    return db.session.query(User).filter(User.id==id).first()


if __name__ == "__main__":
    # set view
    def init_view(app):
        from flask import url_for
        import os
        from flask import send_from_directory

        import common.views
        import user.views
        import conf.views
        
        app.register_blueprint(common.views.blueprint)
        app.register_blueprint(user.views.blueprint)
        app.register_blueprint(conf.views.blueprint)

        @app.route('/')
        def index():
            return render_template('common/index.html')

        @app.route('/favicon.ico')
        def favicon():
            return send_from_directory(os.path.join(app.root_path, 'static'),
                                       'favicon.ico', mimetype='image/vnd.microsoft.icon')

    def init_db():
        from common import db

        import user.models
        import conf.models

        db.Model.metadata.create_all(db.engine)

    def init_controller(app):
        import common.controllers
        import user.controllers
        import conf.controllers
        pass
        
    init_view(app)
    init_db()
    init_controller(app)

    app.run(host='0.0.0.0', port=8000)




