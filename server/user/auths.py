#-*- coding: utf-8 -*-

import httplib
import base64
import json

class GitHubOAuth(object):
    def __init__(self, username='', password='', token=''):
        self.id = username
        self.pw = password
        self.token = token

    def auth_list(self):
        conn = httplib.HTTPSConnection('api.github.com')
        header = {'Authorization': "Basic %s" % base64.encodestring('%s:%s' % (self.id, self.pw))}
        
        conn.request('GET', 
                     '/authorizations', 
                     '{"scopes":[],"note":"Help example"}', 
                     header)
        res = conn.getresponse()
        data = json.loads(res.read())
        conn.close()

        if res.status == 200:
            return True
        else:
            return False

    def create_auth(self):
        # server를 라이브러리 패스로 등록한다
        # oauth key 같은 정보는 저쪽에 집어넣고 ignore를 잘 사용하면
        # oauth key 저장소에 노출시키지 않아도 될거같다
        import os
        import sys
        import inspect
        cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"..")))
        if cmd_subfolder not in sys.path:
            sys.path.insert(0, cmd_subfolder)
        import settings

        ID = self.id
        PW = self.pw
        client_id = settings.GITHUB_CLIENT_ID
        client_secret = settings.GITHUB_CLIENT_SECRET
        conn = httplib.HTTPSConnection('api.github.com')
        header = {"Authorization": "Basic %s" % base64.b64encode('%s:%s' % (ID, PW))}
        body = '{"scopes":["user"],"client_id":"%s","client_secret":"%s"}' % (client_id, client_secret)
        conn.request('POST', '/authorizations', body, header)
        res = conn.getresponse()
        data = json.loads(res.read())
        #print (res.status, res.reason, data)
        conn.close()

        if res.status >= 200 and res.status < 300:
            self.token = data['token']
            return True
        else:
            self.token = ''
            return False

    def user_info(self):
        conn = httplib.HTTPSConnection('api.github.com')
        conn.request('GET', '/user?access_token=%s' % self.token)
        res = conn.getresponse()
        data = json.loads(res.read())
        #print (res.status, res.reason, data)
        conn.close()
        if res.status == 200:
            data['success'] = True
        else:
            data['id'] = 0
            data['success'] = False
        return data
