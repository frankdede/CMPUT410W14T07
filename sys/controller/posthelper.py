import mysql.connector
from databasehelper import *
from authorhelper import *
import utility
class PostHelper:
    """
    #an post helper,which controls the post model
    """
    dbHelper = None;
    def __init__(self,dbHelper):
        self.dbHelper = dbHelper

        """
        to add a post to databse
        dbhelper -- the databasehelper
        post -- the post object
        """
    def addPost(self,post):

        cur = self.dbhelper.getcursor()
        pid = post.getpid()
        aid = post.getaid()
        title = post.gettitle()
        message = post.getmessage()
        type = post.gettype()
        permission = post.getpermission()
        query = "INSERT INTO post VALUES('%s','%s',NULL,'%s','%s','%s','%s')"%(pid,aid,title,message,type,permission)

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except: mysql.connector.Error as err:

          print("SQLException from addPost(): {}".format(err))
          return False

        return cur.rowcount>0

        """add a user permission to post in databse
        dbhelper -- databse helper
        pid -- post id
        aid -- author id
        """
    def addPostPermission(self,dbhelper,pid,aid):

        cur = self.dbHelper.getcursor()
        query = "INSERT INTO user_permission VALUES('%s','%s')"%(pid,aid)

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except: mysql.connector.Error as err:

          print("SQLException from addPost(): {}".format(err))
          return False

        return cur.rowcount>0
#type argument should be one of ['pid','aid','time','message','title','permission']
#Usage: updatepost(databasehelper,pid,type="html", permmision="public") check keyword argument
    def updateMessage(self,pid,newContent):
        """
        to update the message in post
        Keyword arguments:
        dbhelper  -- database helper
        pid -- post id
        newcontent -- the new Content in post
        """
        cur = self.dbHelper.getcursor()
        query = "UPDATE post SET message='%s' WHERE pid='%s'"%(newContent,pid)

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except: mysql.connector.Error as err:

          print("SQLException from addPost(): {}".format(err))
          return False

        return cur.rowcount>0

    def updateTitle(self,pid,newtitle):
        """
        to update the title of post
        pid -- post id
        newtitle -- new title need to be updated
        """
        cur = self.dbHelper.getcursor()
        query = "UPDATE post SET title='%s' WHERE pid='%s'"%(newtitle,pid)

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except: mysql.connector.Error as err:

          print("SQLException from updateTitle(): {}".format(err))
          return False

        return cur.rowcount>0

    def updateTime(self,dbhelper,pid,time = ''):
        """
        to update the time of post
        time -- time format should be like 2014-03-01 01:37:50, the default time is current time.
        """
        cur = self.dbHelper.getcursor()
        if time  == '':
            query = "UPDATE post SET time=NULL WHERE pid='%s'"%(pid)
        else:
            query = "UPDATE post SET time='%s' WHERE pid='%s'"%(time,pid)

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except: mysql.connector.Error as err:

          print("SQLException from updateTime(): {}".format(err))
          return False

        return cur.rowcount>0
# if you need change to permission to user, you need to specify the user aid

    # HAVEN'T BEEN COMPLETED YET
    def updatePermission(self,pid,newPermission,user=''):
        """
        to update the permission
        pid -- post id
        newpermission -- the new permission need to be update
        user -- if the new permission is user, user is the aid
        """
        cur = self.dbHelper.getcursor()
        query = "UPDATE post SET permission='%s' WHERE pid='%s'"%(newPermission,pid)
        cur.execute(query)

        if newPermission == 'user':
            #TODO:Change the following
            #self.addUserPermission(dbhelper,pid,user)
        else:
            query = "DELETE FROM user_permission WHERE pid='%s'"%(pid)

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except: mysql.connector.Error as err:

          print("SQLException from updatePermission(): {}".format(err))
          return False

        return cur.rowcount>0

    def deletePostByPid(self,pid):
        """
         delete a post or server post by pid, aid
        dbhelper -- database helper
        pid -- post id
        """
        cur = self.dbHelper.getcursor()
        query=""
        if type == "pid":
            query = "DELETE FROM post WHERE pid = '%s'"%(key)

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except: mysql.connector.Error as err:

          print("SQLException from deletePostByPid(): {}".format(err))
          return False

        return cur.rowcount>0

    def deletePostByAid(self,aid):
        """
        to delete a post by authorid
        aid -- author id
        dbhelper -- database helper
        """
        cur = self.dbHelper.getcursor()
        query=""
        if type == "aid":
            query = "DELETE FROM post WHERE aid = '%s'"%(aid)

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except: mysql.connector.Error as err:

          print("SQLException from addPost(): {}".format(err))
          return False

        return cur.rowcount>0

    def getPostList(self,aid):
        """
        get list of post that the user by aid can browse
        aid -- author id
        """
        re = []
        cur = self.dbHelper.getcursor()

        #get the post if it is public
        query = "SELECT * FROM post WHERE permission='public'"

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except: mysql.connector.Error as err:

          print("SQLException from getPostList 1st Query: {}".format(err))
          return None

        for fid in cur:
            re.append(fid)

        #???????
        utility.addpath('../model')

        #get the post if aid is its author
        query = "SELECT * FROM post WHERE permission='me' and aid='%s'"%(aid)

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except: mysql.connector.Error as err:

          print("SQLException from getPostList 2nd Query: {}".format(err))
          return None

        for fid in cur:
            re.append(fid)

        #get the post if aid is specifiied user
        query = "SELECT * FROM post WHERE permission = 'user' and pid IN (SELECT pid from user_permission WHERE aid='%s')"%(aid)
        try:
          cur.execute(query)
          self.dbHelper.commit()

        except: mysql.connector.Error as err:

          print("SQLException from getPostList 3rd Query: {}".format(err))
          return None

        for fid in cur:
            re.append(fid)
        #get the post if aid is the author's friend

        authorName = self.getNameByAid(aid)

        query = "SELECT * FROM post WHERE permission = 'friends' and aid IN  (SELECT aid from author WHERE author_name IN (SELECT name1 FROM circle WHERE name2 ='%s' ))"%(authorName)

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except: mysql.connector.Error as err:

          print("SQLException from getPostList 4th Query: {}".format(err))
          return None

        for fid in cur:
            re.append(fid)
        #get the post if aid is the author's friends`s friend

        query = "SELECT * FROM post WHERE permission = 'fof' and aid IN  (SELECT aid from author WHERE author_name IN (SELECT name1 FROM circle WHERE name2 IN (SELECT name1 FROM circle WHERE name2 = '%s')))"%(authorName)

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except: mysql.connector.Error as err:

          print("SQLException from getPostList 5th Query: {}".format(err))
          return None

        for fid in cur:
            re.append(fid)
        #get the post if aid is in the same host as the permission's requirement

        query = "SELECT * FROM post WHERE permission='fomh' AND aid IN (SELECT a1.aid FROM author a1,author a2 WHERE a1.sid = a2.sid AND a2.aid = '%s')"%(aid)

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except: mysql.connector.Error as err:

          print("SQLException from getPostList 6th Query: {}".format(err))
          return None

        for fid in cur:
            re.append(fid)
        return re
