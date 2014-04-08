#!/usr/bin/env python
# coding: utf-8
import subprocess
import unittest
import mysql.connector
import json
import sys,os

sys.path.append("sys/controller")
sys.path.append("sys/model")
# Adapter
from DatabaseAdapter import *
# helpers
from AuthorHelper import *
from CircleHelper import *
from PostHelper import *
from RequestHelper import *
# Controllers 
from AuthorController import *
from RequestController import *
from CommentController import *
from CircleController import *
# models
import author
import post
import time
import Utility
#Flask-Testing
import server
import urllib2
from flask.ext.testing import LiveServerTestCase
from flask.ext.testing import TestCase

DEBUG = True

class ServerTest(unittest.TestCase):

    def setUp(self):
        server.app.config['TESTING'] = True
        # Default port is 5000
        server.app.config['LIVESERVER_PORT'] = 8080
        self.app = server.app.test_client()

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen('http://localhost:8080')
        self.assertEqual(response.code,200)

    def test_server_login(self):
        response = self.app.post('/login',data=dict(username='frank',password='12345'),follow_redirects=True)
        self.assertEqual(json.loads(response.data),{"aid": "111111"})

    def test_server_getCommentsForPost(self):
        self.app.post('/login',data=dict(username='frank',password='12345'),follow_redirects=True)
        response = self.app.get('/author/111111/posts/1/comments/')
        self.assertEqual(response.status_code,200)

    def test_server_admin_page(self):
        self.app.post('/login',data=dict(username='admin',password='12345'),follow_redirects=True)
        response = self.app.get('/000000/admin')
        self.assertEqual(response.status_code,200)

    def test_server_admin_author_delete(self):
        self.app.post('/login',data=dict(username='admin',password='12345'),follow_redirects=True)
        response = self.app.get('/000000/admin/delete/author')
        self.assertEqual(response.status_code,200)

    def test_server_admin_post_delete(self):
        self.app.post('/login',data=dict(username='admin',password='12345'),follow_redirects=True)
        response = self.app.get('/000000/admin/delete/post')
        self.assertEqual(response.status_code,200)

    def test_server_admin_author_approve(self):
        self.app.post('/login',data=dict(username='admin',password='12345'),follow_redirects=True)
        response = self.app.get('/000000/admin/author/approve')
        self.assertEqual(response.status_code,200)

    def test_server_admin_author_deny(self):
        self.app.post('/login',data=dict(username='admin',password='12345'),follow_redirects=True)
        response = self.app.get('/000000/admin/author/deny')
        self.assertEqual(response.status_code,200)

    def test_server_admin_get_post(self):
        self.app.post('/login',data=dict(username='admin',password='12345'),follow_redirects=True)
        response = self.app.get('/000000/admin/view/post')
        self.assertEqual(response.status_code,200)

    def test_server_admin_get_circle(self):
        self.app.post('/login',data=dict(username='admin',password='12345'),follow_redirects=True)
        response = self.app.get('/000000/admin/view/circle')
        self.assertEqual(response.status_code,200)

    def test_server_admin_get_tmp_author(self):
        self.app.post('/login',data=dict(username='admin',password='12345'),follow_redirects=True)
        response = self.app.get('/000000/admin/view/tmp_author')
        self.assertEqual(response.status_code,200)

    #def test_server_admin_change_author(self):
        #self.app.post('/login',data=dict(username='admin',password='12345'),follow_redirects=True)
        #response = self.app.get('/000000/admin/manage/444444',follow_redirects=True)
        #self.assertEqual(response.status_code,200)

    #def test_server_admin_change_signup_policy(self):
        #self.app.post('/login',data=dict(username='admin',password='12345'),follow_redirects=True)
        #response = self.app.get('/000000/admin/global_setting/signup_policy',data=dict(operation='turunon'))
        #self.assertEqual(response.status_code,200)

    def test_server_getuid(self):
        self.app.post('/login',data=dict(username='admin',password='12345'),follow_redirects=True)
        response = self.app.get('/ajax/aid')
        self.assertEqual(response.data,'000000')

    def test_server_getaname(self):
        self.app.post('/login',data=dict(username='admin',password='12345'),follow_redirects=True)
        response = self.app.get('/ajax/author_name')
        self.assertEqual(response.data,'admin')

    #def test_server_register(self):
        #response = self.app.post('/register',data=dict(email='dddd@ulaberta.ca',author_name='ddddd',register_pwd='12345678',nickName=''),follow_redirects=True)
        #print response.data
        #self.assertEqual(response.status_code,200)

    def test_server_authorlist(self):
        self.app.post('/login',data=dict(username='frank',password='12345'),follow_redirects=True)
        response = self.app.get('/111111/recommended_authorlist.json')
        self.assertEqual(response.status_code,200)

    #def test_server_search_author(self):
        #self.app.post('/login',data=dict(username='admin',password='12345'),follow_redirects=True)
        #response = self.app.get('/111111/author/search')
        #self.assertEqual(response.code,200)

    def test_server_allauthorlist(self):
        self.app.post('/login',data=dict(username='frank',password='12345'),follow_redirects=True)
        response = self.app.get('/111111/authorlist.json')
        self.assertEqual(response.status_code,200)

    def test_server_circleauthorlist(self):
        self.app.post('/login',data=dict(username='frank',password='12345'),follow_redirects=True)
        response = self.app.get('/111111/circlelist.json')
        self.assertEqual(response.status_code,200)

    def test_server_render_circle_modal(self):
        self.app.post('/login',data=dict(username='frank',password='12345'),follow_redirects=True)
        response = self.app.get('/111111/circle')
        self.assertEqual(response.status_code,200)

    def test_server_delete_friends(self):
        self.app.post('/login',data=dict(username='frank',password='12345'),follow_redirects=True)
        response = self.app.get('/111111/circle/delete?aid=444444')
        self.assertEqual(response.status_code,200)

    #def test_server_messages(self):
        #self.app.post('/login',data=dict(username='frank',password='12345'),follow_redirects=True)
        #response = self.app.get('/111111/messages.json')
        #self.assertEqual(response.data,'[{"sender_id": "222222", "name": "jack", "time": "2014-04-08 01:29:35"}, {"sender_id": "333333", "name": "william", "time": "2014-04-08 01:29:35"}, {"sender_id": "555555", "name": "paul", "time": "2014-04-08 01:29:35"}]')

    def test_server_messages(self):
        self.app.post('/login',data=dict(username='frank',password='12345'),follow_redirects=True)
        response = self.app.get('/111111/messages.json')
        self.assertEqual(response.status_code,200)

    def test_server_logout(self):
        self.app.post('/login',data=dict(username='frank',password='12345'),follow_redirects=True)
        response = self.app.get('/logout',follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_server_addfriend(self):
        self.app.post('/login',data=dict(username='frank',password='12345'),follow_redirects=True)
        response = self.app.get('/111111/author/request?recipient=444444',follow_redirects=True)
        self.assertTrue(((response.status_code==200)and(response.data=='OK'))or((response.status_code==409)and(response.data=='Existed')))




if __name__ == '__main__':
    unittest.main()
