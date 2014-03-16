#!/usr/bin/env python
import subprocess
import unittest
import mysql.connector
import json
import sys,os
sys.path.append("sys/controller")
sys.path.append("sys/model")
# helpers
from authorhelper import *
from circlehelper import *
from databasehelper import *
from posthelper import *
# models
import author
import post
import time
import utility
DEBUG = True

'''PLEASE rebuild the database everytime before run all the tests!!!'''
class TestController(unittest.TestCase):

    def setUp(self):
        # DO NOT CHANGE HERE
        dbHelper = Databasehelper()
        dbHelper.connect()
        dbHelper.setAutoCommit()

        self.authorhelper = AuthorHelper(dbHelper)
        self.circlehelper = CircleHelper(dbHelper)
        self.posthelper = PostHelper(dbHelper)
    '''
     ====================   AuthorHelper  ====================
     PLEASE rebuild the database before run all the tests!!!
    '''

    def test_authorAuthenticate(self):
        # Tested By: Guanqi
        result = self.authorhelper.authorAuthenticate("frank", "12345")
        self.assertTrue(result == True, "ERROR on authorAuthenticate")

    ''' The best way to avoid collision is to use timestamp'''
    ''' concatnate a string with current time(time in milliseconds)'''
    def test_getAuthorObjectByAid(self):
        result = self.getAuthorObjectByAid("111111")
        self.assertTrue(result.getName()=='frank',"Error on getAuthorObjectByAid")
    def test_getAllAuthorObjectsForLocalServer(self):
        result = self.getAllAuthorObjectsForLocalServer()
        self.assertTrue(result!=None,"ERROR on getAllAuthorObjectsForLocalServer")
    def test_getAllAuthorObjectsForRemoteServer(self):
        result = self.getAllAuthorObjectsForRemoteServer()
        self.assertTrue(result!=None,"ERROR on getAllAuthorObjectsForRemoteServer")
    def test_addLocalAuthor(self):
        result = self.authorhelper.addLocalAuthor("coniewti1", "201486", "Conie")
        self.assertTrue(result != None, "ERROR on addAuthor")
    # need a add remote author
    def test_updateNickNameByAid(self):
        # Tested By : Guanqi
        result = self.authorhelper.updateNickNameByAid("111111", "nickname"+str(int(time.time()*1000)))
        self.assertTrue(result == True, "ERROR on updateNickName")
    
    def test_updateUpdatePasswordByAid(self):
        # Tested By : Guanqi
        result = self.authorhelper.updatePasswordByAid("111111","password"+str(int(time.time()*1000)))
        self.assertTrue(result == True, "ERROR on updatePassword")
        
    
    ''' Here is a good example for you to test both add and delete API '''
    ''' Test your insert methods before test the delete ones '''

    def test_addAndDeleteAuthor(self):
        # Tested By : Guanqi
        result = self.authorhelper.addAuthor("coniewt", "201486", "Conie")
        self.assertTrue(result != None, "ERROR on addAuthor")

        # Tested By : Guanqi
        # JASON ENCODING EXAMPLE:
        # In order to decode the json object, call function json.loads(your_josn_object)
        # and then it will return a dictionary object.

        result = self.authorhelper.deleteAuthor(json.loads(result)["aid"])
        self.assertTrue(result == True, "ERROR on deleteAuthor")

    '''
     ====================   CircleHelper  ====================
     PLEASE rebuild the database before run all the tests!!!
    '''

    def test_getFriendList(self):
        # Tested By : Guanqi
        friends = self.circlehelper.getFriendList('111111')
        friendsObj= author.parseList(friends)

        for friend in friendsObj:
            self.assertTrue(friend.getName() != None,"ERROR on getFriendList ")
            self.assertTrue(friend.getAid() != None,"ERROR on getFriendList")

    def test_getFriendOfFriendList(self):
        # Tested By : Guanqi
        friends = self.circlehelper.getFriendOfFriendList('111111')
        print(friends)
        for friend in friendsObj:
            self.assertTrue(friend.getName() != None,"ERROR on getFriendList ")
            self.assertTrue(friend.getAid() != None,"ERROR on getFriendList")


    '''
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
