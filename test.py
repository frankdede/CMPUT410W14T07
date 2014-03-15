#!/usr/bin/env python
import unittest
import mysql.connector
import json
import sys,os
sys.path.append("sys/controller")
sys.path.append("sys/model")
from authorhelper import *
from circlehelper import *
from databasehelper import *
from posthelper import *
import time
import utility
import post
DEBUG = True

'''PLEASE rebuild the database everytime before run all the tests!!!'''
class TestController(unittest.TestCase):

    def setUp(self):
        
        dbHelper = Databasehelper()
        dbHelper.connect()
        dbHelper.setAutoCommit()

        self.authorhelper = AuthorHelper(dbHelper)
        self.circlehelper = CircleHelper(dbHelper)
        self.posthelper = PostHelper(dbHelper)

    def test_authorAuthenticate(self):
        # Test By: Guanqi
        result = self.authorhelper.authorAuthenticate("frank", "12345")
        self.assertTrue(result == True, "ERROR on authorAuthenticate")
    
    def test_updateNickNameByAid(self):
        # Test By : Guanqi 
        result = self.authorhelper.updateNickNameByAid("111111", "nickname"+str(int(time.time()*1000)))
        self.assertTrue(result == True, "ERROR on updateNickName")
    
    def test_updateUpdatePasswordByAid(self):
        # Test By : Guanqi
        result = self.authorhelper.updatePasswordByAid("111111","password"+str(int(time.time()*1000)))
        self.assertTrue(result == True, "ERROR on updatePassword")
        
    def test_addAndDeleteAuthor(self):
        # Test By : Guanqi
        result = self.authorhelper.addAuthor("coniewt", "201486", "Conie")
        self.assertTrue(result != None, "ERROR on addAuthor")

        # Test By : Guanqi
        result = self.authorhelper.deleteAuthor(json.loads(result)["aid"])
        self.assertTrue(result == True, "ERROR on deleteAuthor")

'''PLEASE rebuild the database everytime before run all the tests!!!'''
    '''    
    def testcicle(self):
        add = self.circlehelper.addNewCircle("frank", "mark")
        self.assertTrue(add == True, "ERROR on addnewcircle")
        
        add = self.circlehelper.addNewCircle("frank", "owen")
        self.assertTrue(add == True, "ERROR on addnewcircle")

        delete = self.circlehelper.deleteCircle("frank", "mark")
        self.assertTrue(delete == True, "ERROR on deletecircle")
        
        rm = self.circlehelper.removeCircle("frank")
        self.assertTrue(rm == True, "ERROR on removecircle")
        
        getfrd = self.circlehelper.getFriendList("Mary")
        self.assertTrue(getfrd != None, "ERROR on getfriendlist")
        
        getfof = self.circlehelper.getFriendOfFriend("Mary")
        self.assertTrue(getfof != None, "ERROR on getfriendoffriend")
        
    def testpost(self):
        add = self.posthelper.addPost(Post('p4','111111','2014-03-10 20:52:51','hello','msg','text','public'))
        self.assertTrue(add == True, "ERROR on insertpost")
        
        updmsg = self.posthelper.updateMessage("p4", "newcontent"+str(randint(0,100000000000)))
        self.assertTrue(updmsg == True, "ERROR on updateMessage")

        updtle = self.posthelper.updateTitle("p4", "newtitle"+str(randint(0,100000000000)))
        self.assertTrue(updtle == True, "ERROR on updateTitle")

        #updpms = self.posthelper.updatePermission("p4", "friends")
        #self.assertTrue(updpms == True, "ERROR on updatePermission")

        delpid = self.posthelper.deletePostByPid("p4")
        self.assertTrue(delpid == True, "ERROR on deletepostbyid")

        #addpms = self.posthelper.addPostPermission("pid", "aid")
        #self.assertTrue(addpms == True, "ERROR on addpostpermission")
        getpstlst = self.posthelper.getPostList("111111")
        self.assertTrue(getpstlst != None, "ERROR on getpostlist")

        delaid = self.posthelper.deletePostByAid("111111")
        self.assertTrue(delaid == True, "ERROR on deletepostbyaid")
      '''  
        

if __name__ == '__main__':
        unittest.main()
