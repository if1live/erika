#-*- coding: utf-8 -*-

import flask
blueprint = flask.Blueprint('user', __name__, url_prefix='/user',
                            template_folder='templates')

from flask import (
    render_template, request, redirect, url_for, flash, session
    )
from user.models import (
    User
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
from user.controllers import *
from auths import twitter, google, github
import constants


@blueprint.route("/")
def index():
    return render_template("user/index.html")

@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))

def del_token_session():
    for key in constants.KEY_OAUTH_TOKEN_LIST:
        if key in session:
            session.pop(key)

@blueprint.route('/login/twitter')
def login_twitter():
    logout_user()
    # 기존에 남아잇는 twitter oauth때문에 다시 로그인하는거 깨질지 모르니까
    # 완전히 파기하자
    del_token_session()

    return twitter.authorize(
        callback=url_for('user.authorized_twitter',
                         next=request.args.get('next') 
                         or request.referrer or None))

@blueprint.route('/authorized/twitter')
@twitter.authorized_handler
def authorized_twitter(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session[constants.KEY_TWITTER_OAUTH_TOKEN] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )

    info = OAuthSignUpInfo.create_with_twitter_resp(resp)
    user_oauth = info.get_oauth_info()
    if UserOAuthController.is_exist(user_oauth) is True:
        # 이미 한번 로그인을 한 경우, 연결된 User를 찾아서 로그인 처리
        prev_oauth = UserOAuthController.get(user_oauth)
        prev_oauth.extra = resp
        prev_oauth.oauth_token = resp['oauth_token']
        db.session.commit()
        
        user_obj = prev_oauth.user
        if login_user(user_obj, remember=True):
            return redirect(next_url)
        else:
            return 'Not valid User?'
    else:
        # 로그인 한적 없는 유저의 경우, 새로 가입해야한다
        # 새로 가입하는 페이지로 이동. 동시에 현재 얻은 객체는 적절히
        # 어딘가에 저장시켜놧다가 가입페이지에서 재사용한다
        return oauth_signup(info, next_url)
    

@blueprint.route('/login/google')
def login_google():
    logout_user()
    del_token_session()

    # google oauth의 경우, url에 추가 정보를 달아놓으면
    # URL에서 에러를 뱉는다. 그래서 next를 따로 세션에 넣어놧다가 꺼내서 쓰자
    next_url = request.args.get('next') or request.referrer or None
    session['google-next-url'] = next_url
    
    callback = url_for('.authorized_google', _external=True)
    return google.authorize(callback=callback)

@blueprint.route('/authorized/google')
@google.authorized_handler
def authorized_google(resp):
    next_url = session['google-next-url']
    del session['google-next-url']

    if resp is None:
        flash(u'You denied the request to sign in')
        return redirect(next_url)

    access_token = resp['access_token']
    session[constants.KEY_GOOGLE_OAUTH_TOKEN] = (access_token, '')
    info = OAuthSignUpInfo.create_with_google_resp(resp)

    user_oauth = info.get_oauth_info()
    if UserOAuthController.is_exist(user_oauth) is True:
        prev_oauth = UserOAuthController.get(user_oauth)
        prev_oauth.extra = resp
        prev_oauth.oauth_token = resp['access_token']
        db.session.commit()
        
        user_obj = prev_oauth.user
        if login_user(user_obj, remember=True):
            return redirect(next_url)
        else:
            return 'Not valid User?'
    else:
        return oauth_signup(info, next_url)

@blueprint.route('/login/github')
def login_github():
    logout_user()
    del_token_session()

    # google oauth의 경우, url에 추가 정보를 달아놓으면
    # URL에서 에러를 뱉는다. 그래서 next를 따로 세션에 넣어놧다가 꺼내서 쓰자
    next_url = request.args.get('next') or request.referrer or None
    callback = url_for('.authorized_github', _next=next_url)
    return github.authorize(callback=callback)

@blueprint.route('/authorized/github')
@github.authorized_handler
def authorized_github(resp):
    print 'resp'
    return 'fdsf'


def oauth_signup(info, next_url):
    name = UserController.get_valid_name(info.name)

    user = User(name, info.email)
    db.session.add(user)
    db.session.commit()

    user_oauth = info.get_oauth_info()
    user_oauth.user = user
    db.session.add(user_oauth)
    db.session.commit()

    login_user(user, remember=True)
    flash('%s Sign Up Complete' % name)
    return redirect(next_url or url_for("index"))


class OAuthSignUpInfo(object):
    def __init__(self):
        self.oauth_token = None
        self.oauth_extra = {}
        self.provider = ''
        self.provider_uid = ''

        self.name = ''
        self.email = ''
        
    def get_oauth_info(self):
        obj = UserOAuth(self.provider, self.provider_uid,
                         self.oauth_token, self.oauth_extra)
        return obj

    @classmethod
    def create_with_twitter_resp(cls, resp):
        info = cls()
        info.provider = constants.PROVIDER_TWITTER
        info.provider_uid = resp['user_id']
        info.name = resp['screen_name']
        info.oauth_token = resp['oauth_token']
        info.oauth_extra = resp
        return info

    @classmethod
    def create_with_google_resp(cls, resp):
        info = cls()
        info.provider = constants.PROVIDER_GOOGLE
        info.oauth_token = resp['access_token']
        info.oauth_extra = resp

        data = GoogleProfileFetcher(resp['access_token']).fetch()
        info.provider_uid = data['id']
        if data['verified_email'] == True:
            info.email = data['email']

        name_candidate_list = [
            data['name'],
            data['email']
            ]
        for name in name_candidate_list:
            if len(name) > 0:
                info.name = name
                break

        return info

class GoogleProfileFetcher(object):
    def __init__(self, access_token):
        self.access_token = access_token

    def fetch(self):
         from urllib2 import Request, urlopen, URLError
         import json

         headers = {'Authorization': 'OAuth '+self.access_token}
         req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                       None, headers)
         try:
             res = urlopen(req)
             data = res.read()
             return json.loads(data)
         except URLError, e:
             if e.code == 401:
                 # Unauthorized - bad token
                 session.pop('access_token', None)
                 return redirect(url_for('login'))
             return res.read()



"""
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
            user_obj = UserController.get_github_user(info['id'])
            if user_obj is None:
                # 없으면 적절히 새로 만들기
                user_obj = User(info['login'])
                user_obj.provider = PROVIDER_GITHUB
                user_obj.token = oauth.token
                user_obj.provider_userid = unicode(info['id'])
                user_obj.profile = info
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
    return redirect(url_for('index'))


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
    return redirect(url_for("index"))

"""
