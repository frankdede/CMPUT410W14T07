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
        server.app.config['LIVESERVER_PORT'] = 5000
        self.app = server.app.test_client()

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen('http://localhost:5000')
        self.assertEqual(response.code,200)

    def test_server_login(self):
        response = self.app.post('/login',data=dict(username='frank',password='12345'),follow_redirects=True)
        self.assertEqual(json.loads(response.data),{"aid": "111111"})

    def test_server_getCommentsForPost(self):
        pass



if __name__ == '__main__':
    unittest.main()
