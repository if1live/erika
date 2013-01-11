#-*- coding: utf-8 -*-

import flask
blueprint = flask.Blueprint('user', __name__, url_prefix='/user',
                            template_folder='templates')

from flask import (
    render_template, request, redirect, url_for, flash
    )
from user.models import (
    User, AnonymousUser
    )

from flask.ext.login import (
    login_user,
    login_required,
    current_user,
    logout_user,
    confirm_login,
    fresh_login_required,
    )
'''
@blueprint.route('/')
def index():
    return render_template('common/base.html')

@blueprint.route('/login/<name>', methods=['GET', 'POST'])
def login(name):
    #    if request.method == 'POST' and 'username' in request.form:
    #       username = request.form['username']
    u = User(1, 'myname', 'fdsf')
    login_user(u, True)
    print current_user()
        
    return 'login : %s' % name


@blueprint.route('/logout')
@login_required
def logout():
    #logout_user()
    #flash('Log out')
    return 'logout'
#return redirect(url_for('index'))
'''

@blueprint.route("/")
def index():
    return render_template("user/index.html")


@blueprint.route("/secret")
@fresh_login_required
def secret():
    return render_template("user/secret.html")


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    from main import USERS, USER_NAMES

    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        if username in USER_NAMES:
            remember = request.form.get("remember", "no") == "yes"
            if login_user(USER_NAMES[username], remember=remember):
                flash("Logged in!")
                return redirect(request.args.get("next") or url_for("user.index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username.")
    return render_template("user/login.html")


@blueprint.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("user.index"))
    return render_template("user/reauth.html")


@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("user.index"))
