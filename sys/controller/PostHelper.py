import mysql.connector
from DatabaseAdapter import *
from AuthorHelper import *
import Utility
import sys
sys.path.append("sys/model")
from post import *
import json
class PostHelper:
  
    dbAdapter = None
    def __init__(self,dbAdapter):
        self.dbAdapter = dbAdapter

    def addPost(self,aid,title,content,type,permission):

        cur = self.dbAdapter.getcursor()

        pid = utility.getid()

        query = "INSERT INTO post VALUES('%s','%s',NULL,'%s','%s','%s','%s')"%(pid,aid,title,content,type,permission)

        try:
          cur.execute(query)

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from addPost():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return None

        if cur.rowcount>0:
          return True
        else:
          return False
          
    def addPostPermission(self,dbAdapter,pid,aid):

        cur = self.dbAdapter.getcursor()
        query = "INSERT INTO user_permission VALUES('%s','%s')"%(pid,aid)

        try:

          cur.execute(query)
          self.dbAdapter.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException is raised by addPostPermission():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        return cur.rowcount>0
#type argument should be one of ['pid','aid','time','message','title','permission']
#Usage: updatepost(databasehelper,pid,type="html", permmision="public") check keyword argument
    def updateMessage(self,pid,newContent):
      
        cur = self.dbAdapter.getcursor()
        query = "UPDATE post SET message='%s' WHERE pid='%s'"%(newContent,pid)

        try:
          cur.execute(query)
          self.dbAdapter.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException is raised by updateMessage():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        return cur.rowcount>0

    def updateTitle(self,pid,newtitle):
        
        cur = self.dbAdapter.getcursor()
        query = "UPDATE post SET title='%s' WHERE pid='%s'"%(newtitle,pid)

        try:
          cur.execute(query)
          self.dbAdapter.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException is raised by updateTime():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        return cur.rowcount>0

    def updateTime(self,dbAdapter,pid,time = ''):
        
        cur = self.dbAdapter.getcursor()
        if time  == '':
            query = "UPDATE post SET time=NULL WHERE pid='%s'"%(pid)
        else:
            query = "UPDATE post SET time='%s' WHERE pid='%s'"%(time,pid)

        try:
          cur.execute(query)
          self.dbAdapter.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException is raised by updateTime():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")

          return False

        return cur.rowcount>0
# if you need change to permission to user, you need to specify the user aid

    # HAVEN'T BEEN COMPLETED YET
    def updatePermission(self,pid,newPermission,user=''):
        
        cur = self.dbAdapter.getcursor()
        query = "UPDATE post SET permission='%s' WHERE pid='%s'"%(newPermission,pid)
        cur.execute(query)

        if newPermission == 'user':
            #TODO:Change the following
            print("neeed to be fixed")
            #self.addUserPermission(dbAdapter,pid,user)
        else:
            query = "DELETE FROM user_permission WHERE pid='%s'"%(pid)

        try:
          cur.execute(query)
          self.dbAdapter.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException is raised by updatePermission():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        return cur.rowcount>0

    def deletePostByPid(self,pid):
       
        cur = self.dbAdapter.getcursor()
        query = "DELETE FROM post WHERE pid = '%s'"%(pid)

        try:
          cur.execute(query)
          self.dbAdapter.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException is raised by deletePostByPid():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        return cur.rowcount>0

    def deletePostByAid(self,aid):
        
        cur = self.dbAdapter.getcursor()
        query = "DELETE FROM post WHERE aid = '%s'"%(aid)

        try:
          cur.execute(query)
          self.dbAdapter.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException is raised by deletePostByAid():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        return cur.rowcount>0
    def getPublicPost(self,aid):
        re = []
        cur = self.dbAdapter.getcursor()
        
        #get the post if it is public
        query = "SELECT pid,aid,time,title,content,type,permission FROM post WHERE permission='public';"
        try:
            cur.execute(query)
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from getPublicPost():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("1st Query:",query)
            print("****************************************")
            return None
        if cur != None:
            for ele in cur:
                pid = ele[0]
                aid = ele[1]
                time = ele[2].strftime("%Y-%m-%d %H:%M:%S")
                title = ele[3]
                msg = ele[4]
                msgType = ele[5]
                permission = ele[6]
                post = Post(pid,aid,time,title,msg,msgType,permission)
                re.append(post)
            return re 
    def getPrivatePost(self,aid):
        re = []
        cur = self.dbAdapter.getcursor()
        
        #get the post if it is public
        query = "SELECT pid,aid,time,title,content,type,permission FROM post WHERE permission='me' AND aid='%s';"%(aid)
        try:
            cur.execute(query)
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from getPublicPost():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("1st Query:",query)
            print("****************************************")
            return None
        if cur != None:
            for ele in cur:
                pid = ele[0]
                aid = ele[1]
                time = ele[2].strftime("%Y-%m-%d %H:%M:%S")
                title = ele[3]
                msg = ele[4]
                msgType = ele[5]
                permission = ele[6]
                post = Post(pid,aid,time,title,msg,msgType,permission)
                re.append(post)
            return re
    def getFriendsFriendPost(self,aid):
        re = []
        cur = self.dbAdapter.getcursor()
        
        #get the post if it is public
        query = "SELECT pid,aid,time,title,content,type,permission FROM post WHERE permission='fof' AND aid IN (SELECT aid1 FROM circle WHERE aid2 IN (SELECT aid1 FROM circle WHERE aid2='%s'));"%(aid)
        try:
            cur.execute(query)
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from getPublicPost():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("1st Query:",query)
            print("****************************************")
            return None
        if cur != None:
            for ele in cur:
                pid = ele[0]
                aid = ele[1]
                time = ele[2].strftime("%Y-%m-%d %H:%M:%S")
                title = ele[3]
                msg = ele[4]
                msgType = ele[5]
                permission = ele[6]
                post = Post(pid,aid,time,title,msg,msgType,permission)
                re.append(post)
            return re
    def getFriendsPost(self,aid):
        re = []
        cur = self.dbAdapter.getcursor()
        #get the post if it is public
        query = "SELECT pid,aid,time,title,content,type,permission FROM post WHERE permission='friends' AND aid IN (SELECT aid1 FROM circle WHERE aid2 ='%s');"%(aid)
        try:
            cur.execute(query)
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from getPublicPost():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("1st Query:",query)
            print("****************************************")
            return None
        if cur != None:
            for ele in cur:
                pid = ele[0]
                aid = ele[1]
                time = ele[2].strftime("%Y-%m-%d %H:%M:%S")
                title = ele[3]
                msg = ele[4]
                msgType = ele[5]
                permission = ele[6]
                post = Post(pid,aid,time,title,msg,msgType,permission)
                re.append(post)
            return re
    def getAuthorPost(self,aid):
        re = []
        cur = self.dbAdapter.getcursor()
        #get the post if it is public
        query = "SELECT pid,aid,time,title,content,type,permission FROM post WHERE permission='author' AND pid IN (SELECT pid FROM post_permission WHERE aid ='%s');"%(aid)
        try:
            cur.execute(query)
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from getAuthorPost():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Query:",query)
            print("****************************************")
            return None
        if cur != None:
            for ele in cur:
                pid = ele[0]
                aid = ele[1]
                time = ele[2].strftime("%Y-%m-%d %H:%M:%S")
                title = ele[3]
                msg = ele[4]
                msgType = ele[5]
                permission = ele[6]
                post = Post(pid,aid,time,title,msg,msgType,permission)
                re.append(post)
            return re
    def getMyHostFriendPost(self,aid):
        re = []
        cur = self.dbAdapter.getcursor()
        #get the post if it is public
        query = "SELECT pid,aid,time,title,content,type,permission FROM post WHERE permission='fomh' AND aid IN (SELECT aid1 FROM circle WHERE aid2='%s') AND EXISTS (SELECT * FROM author WHERE aid='%s' AND sid =1);"%(aid,aid)
        try:
            cur.execute(query)
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from getAuthorPost():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Query:",query)
            print("****************************************")
            return None
        if cur != None:
            for ele in cur:
                pid = ele[0]
                aid = ele[1]
                time = ele[2].strftime("%Y-%m-%d %H:%M:%S")
                title = ele[3]
                msg = ele[4]
                msgType = ele[5]
                permission = ele[6]
                post = Post(pid,aid,time,title,msg,msgType,permission)
                re.append(post)
            return re
