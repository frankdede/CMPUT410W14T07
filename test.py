#!/usr/bin/env python
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
from RequestController import *
from CommentController import *
from CircleController import *
# models
import author
import post
import time
import Utility
DEBUG = True

'''PLEASE rebuild the database everytime before run all the tests!!!'''
class TestController(unittest.TestCase):

    def setUp(self):
        # DO NOT CHANGE HERE
        dbAdapter = DatabaseAdapter()
        dbAdapter.connect()
        dbAdapter.setAutoCommit()
        # helpers
        self.authorHelper = AuthorHelper(dbAdapter)
        self.circleHelper = CircleHelper(dbAdapter)
        self.postHelper = PostHelper(dbAdapter)
        self.requestHelper = RequestHelper(dbAdapter)
        # controllers
        self.commentController = CommentController(dbAdapter)
        self.requestController = RequestController(dbAdapter)
        self.circleHelper = CircleHelper(dbAdapter)

    '''
     ====================   AuthorHelper  ====================
     PLEASE rebuild the database before run all the tests!!!
    '''


    '''
     ====================   RequestHelper  ====================
     PLEASE rebuild the database before run all the tests!!!
    '''

    def test_addNewRequest(self):
        # Tested By : Guanqi
        result = self.requesthelper.addNewRequest('222222','111111')
        requestObj = json.loads(result)
        self.assertTrue(requestObj['recipient_id'] =='222222',"ERROR on addNewRequest ")
        self.assertTrue(requestObj['sender_id'] == '111111',"ERROR on addNewRequest ")


    '''
     ====================   CommentHelper  ====================
     PLEASE rebuild the database before run all the tests!!!
    '''

if __name__ == '__main__':
        unittest.main()
