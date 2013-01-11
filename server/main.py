#-*- coding: utf-8 -*-

from flask import Flask
import settings

app = Flask(__name__)
app.debug = settings.DEBUG
app.secret_key = settings.APP_SECRET_KEY

if __name__ == '__main__':
    import common.views
    import user.views

    app.register_blueprint(common.views.blueprint)
    app.register_blueprint(user.views.blueprint)

    app.run(host='0.0.0.0', port=8000)

