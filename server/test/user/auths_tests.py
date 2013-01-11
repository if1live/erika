#-*- coding: utf-8 -*-

import unittest
from user import auths
import getpass

class GitHubOAuthTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.id = raw_input('GitHub id : ')
        cls.pw = getpass.getpass('Password for %s : ' % cls.id)
        
        # 토큰을 매번 재생성하는건 느리니까
        # 테스트를 잘 구성해서 1번만 생성해서 재탕하도록 하자
        cls.token = cls.run_create_auth()

    def test_user_info(self):
        oauth = auths.GitHubOAuth(token=self.token)
        info = oauth.user_info()
        self.assertTrue(info['id'] > 0)
        self.assertEqual(True, info['success'])

        oauth = auths.GitHubOAuth(token='fdsfdsfd')
        info = oauth.user_info()
        self.assertEqual(0, info['id'])
        self.assertEqual(False, info['success'])

    def test_empty(self):
        pass

    @classmethod
    def run_create_auth(cls):        
        oauth = auths.GitHubOAuth(cls.id, cls.pw)
        retval = oauth.create_auth()
        return oauth.token



