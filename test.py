#!/usr/bin/env python

import mysql.connector
import json
import sys,os
sys.path.append("sys/controller")
sys.path.append("sys/model")
from authorhelper import *
from circlehelper import *
from databasehelper import *
from posthelper import *
from random import randint
import utility
import post
DEBUG = True

import unittest
# confict !
# rebuild the database before run this test
class TestController(unittest.TestCase):

    def setUp(self):
        
        dbHelper = Databasehelper()
        dbHelper.connect()
        dbHelper.setAutoCommit()

        self.authorhelper = AuthorHelper(dbHelper)
        self.circlehelper = CircleHelper(dbHelper)
        self.posthelper = PostHelper(dbHelper)

    def testauthor(self):
        author = self.authorhelper.authorAuthenticate("frank", "12345")
        self.assertTrue(author == True, "ERROR on authorauthenticate")
        
        name = self.authorhelper.doesAuthorExist("frank")
        self.assertTrue(name == True, "ERROR on checkauthorexist")
        
        aid = self.authorhelper.getAidByAuthorName("frank")
        self.assertTrue(aid != None, "ERROR on getaidbyname")
        
        name = self.authorhelper.getAuthorNameByAid("111111")
        self.assertTrue(name != None, "ERROR on getnamebyaid")
        
        update = self.authorhelper.updateNickNameByAid("111111", "newnickname"+str(randint(0,100000000000)))
        self.assertTrue(update == True, "ERROR on updateNickName")
        
        update = self.authorhelper.updatePasswordByAid("222222", str(randint(0,100000000000)))
        self.assertTrue(update == True, "ERROR on updatepassword")
        
        add = self.authorhelper.addAuthor("coniewt", "201486", "Conie")
        self.assertTrue(add == True, "ERROR on addauthor")

        delete = self.authorhelper.deleteAuthor("coniewt")
        self.assertTrue(delete == True, "ERROR on deleteauthor")
        
        
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
        
        

if __name__ == '__main__':
        unittest.main()
