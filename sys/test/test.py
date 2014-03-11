#!/usr/bin/env python

import mysql.connector
import json
sys.path.append('sys/controller')
import AuthorHelper
import CircleHelper
import Databasehelper
import PostHelper
import utility
DEBUG = True
import sys,os
import unittest

class TestController(unittest.TestCase):
    
    def __init__(self):
        self.authorhelper = AuthorHelper()
        self.circlehelper = CircleHelper()
        self.msghelper = Messagehelper()
        self.posthelper = PostHelper()
        
    def testauthor(self):
        author = authorhelper.authorAuthenticate("coniewt", "pwd")
        self.assertTrue(author == False, "ERROR on authorauthenticate")
        
        name = authorhelper.doesAuthorExist("coniewt")
        self.assertTrue(name == False, "ERROR on checkauthorexist")
        
        aid = authorhelper.getAidByAuthorName("Rose")
        self.assertTrue(aid != None, "ERROR on getaidbyname")
        
        name = authorhelper.getAuthorNameByAid(aid)
        self.assertTrue(name == "Rose", "ERROR on getnamebyaid")
        
        update = authorhelper.updateNickNameByUserId("Rose", "newnickname")
        self.assertTrue(update == True, "ERROR on updateNickName")
        
        update = authorhelper.updatePasswordByUserId(aid, "newpassword")
        self.assertTrue(update == True, "ERROR on updatepassword")
        
        delete = authorhelper.deleteAuthor("Rose")
        self.assertTrue(delete == True, "ERROR on deleteauthor")
        
        add = authorhelper.addAuthor("coniewt", "201486", "Conie")
        self.assertTrue(add == True, "ERROR on addauthor")
        
    def testcicle(self):
        add = circlehelper.addNewCircle("coniewt", "Mary")
        self.assertTrue(add == True, "ERROR on addnewcircle")
        
        delete = circlehelper.deleteCircle("coniewt", "Mary")
        self.assertTrue(delete == True, "ERROR on deletecircle")
        
        rm = circlehelper.removeCircle("coniewt")
        self.assertTrue(rm == True, "ERROR on removecircle")
        
        getfrd = circlehelper.getFriendList("Mary")
        self.assertTrue(getfrd != None, "ERROR on getfriendlist")
        
        getfof = circlehelper.getFriendOfFriend("Mary")
        self.assertTrue(getfof != None, "ERROR on getfriendoffriend")
        
    def testpost(self):
        add = posthelper.addPost(("pid", "aid", "title", "msg", "html", "me"))
        self.assertTrue(add == True, "ERROR on insertpost")
        
        addpms = posthelper.addPostPermission("pid", "aid")
        self.assertTrue(addpms == True, "ERROR on addpostpermission")
        
        updmsg = posthelper.updateMessage("pid", "newcontent")
        self.assertTrue(updmsg == True, "ERROR on updateMessage")
        
        updtle = posthelper.updateTitle("pid", "newtitle")
        self.assertTrue(updtle == True, "ERROR on updateTitle")
        
        updtime = posthelper.updateTime("pid", "2014-03-01 01:37:50")
        self.assertTrue(updtime == True, "ERROR on updateTime")
        
        updpms = posthelper.updatePermission("pid", "friends")
        self.assertTrue(updpms == True, "ERROR on updatePermission")
        
        delpid = posthelper.deletePostByPid("pid")
        self.assertTrue(delpid == True, "ERROR on deletepostbyid")
        
        delaid = posthelper.deletePostByAid("aid")
        self.assertTrue(delaid == True, "ERROR on deletepostbyaid")
        
        getpstlst = posthelper.getPostList("aid")
        self.assertTrue(getpstlst != None, "ERROR on getpostlist")

if __name__ == '__main__':
    unittest.main()