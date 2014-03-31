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
import urllib2
from flask.ext.testing import LiveServerTestCase
from flask.ext.testing import TestCase
DEBUG = True

class ServerTest(unittest.TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        # Default port is 5000
        app.config['LIVESERVER_PORT'] = 5000
        return app

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen('http://localhost:5000')
        self.assertEqual(response.code,200)

if __name__ == '__main__':
    unittest.main()
