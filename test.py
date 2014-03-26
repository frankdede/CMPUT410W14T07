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
        self.cid = None
        self.aid = None
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
    
    def test_sendRequest(self):
        # Tested By : Guanqi
        result = self.requestController.sendRequest('111111','222222')
        self.assertTrue(result == True,"Failed to sent a request")
    
    
    def test_accpetRequestFromSender(self):
        result = self.requestController.acceptRequestFromSender('111111','222222')
        self.assertTrue(result == True,"Failed to accept a request from sender")
    
    '''
    Cannot delete request by far
    def test_deleteRequest(self):
        result = self.requestController.deleteRequest('222222','111111')
        self.assertTrue(result == True,"Failed to delete a request")
    '''

    '''
     ====================   CommentHelper  ====================
     PLEASE rebuild the database before run all the tests!!!
    '''

    def test_getAllCommentsForPost(self):
    # Tested By : Guanqi
        result = self.commentController.getAllCommentsForPost('1')
        self.assertTrue(result != None,"Failed to get all comments for post")

    def test_addCommentForPost(self):
    # Tested By : Guanqi
        cid = self.commentController.addCommentForPost('111111','1','Hello')

        self.assertTrue(cid != None,"Failed to add comment for post")

    def test_deleteCommentForPost(self):

        result = self.commentController.deleteCommentForPost('1')
        self.assertTrue(result == True,"Failed to delete comment for post")


if __name__ == '__main__':
    print("**************************** Script Starts ****************************")
    subprocess.call(["./install.sh", "-rebuild_all"])
    print("**************************** Script Ends *********************************")
    print("**************************** Test Starts *********************************")
    unittest.main()
        