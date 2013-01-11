#-*- coding: utf-8 -*-

from flask import Flask
import settings

app = Flask(__name__)
app.debug = settings.DEBUG
app.secret_key = settings.APP_SECRET_KEY

if __name__ == '__main__':
    # ser view
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
