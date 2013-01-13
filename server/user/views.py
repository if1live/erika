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

from common import db


@blueprint.route("/")
def index():
    return render_template("user/index.html")


@blueprint.route("/secret")
@fresh_login_required
def secret():
    return render_template("user/secret.html")


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        #if username in USER_NAMES:
        remember = request.form.get("remember", "no") == "yes"
        # force login
        if login_user(User(1, 'asd'), remember=remember):
            flash("Logged in!")
            return redirect(request.args.get("next") or url_for("user.index"))
        else:
            flash("Sorry, but you could not log in.")
        #else:
        #    flash(u"Invalid username.")
    return render_template("user/login.html")

@blueprint.route('/login/github', methods=['GET', 'POST'])
def login():
    if request.method in ('POST', 'GET') and 'userid' in request.form:
        userid = request.form['userid']
        passwd = request.form['passwd']

        from user import auths
        oauth = auths.GitHubOAuth(userid, passwd)
        retval = oauth.create_auth()
        if retval is True:
            # 로그인 가능한 사용자면 db에 존재하는지 일단 확인하기
            info = oauth.user_info()
            
            # 해당 서비스를 사용하는 유저가 이니 존재하는지 확인하기
            from user.models import PROVIDER_GITHUB
            user_obj = User.get_oauth_user(PROVIDER_GITHUB, info['id'])
            if user_obj is None:
                # 없으면 적절히 새로 만들기
                user_obj = User(info['login'])
                user_obj.provider = PROVIDER_GITHUB
                user_obj.token = oauth.token
                user_obj.provider_userid = unicode(info['id'])
                user_obj.github_user_info = info
                db.session.add(user_obj)
                db.session.commit()
            else:
                user_obj.token = oauth.token
                db.session.commit()
            
            if login_user(user_obj, remember=True):
                flash('Logged in')
            else:
                flash("Sorry, but you could not log in.")                
        else:
            flash(u'Invalid GitHub userid')
    return redirect(url_for('common.index'))


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
    return redirect(url_for("common.index"))

