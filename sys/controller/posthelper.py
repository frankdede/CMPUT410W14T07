import mysql.connector
from databasehelper import *
from authorhelper import *
import utility
import sys
sys.path.append("sys/model")
from post import *
import json
class PostHelper:
    """
    #an post helper,which controls the post model
    """
    dbHelper = None
    def __init__(self,dbHelper):
        self.dbHelper = dbHelper

        """
        to add a post to databse
        dbhelper -- the databasehelper
        post -- the post object
        """
    def addPost(self,aid,title,content,type,permission):

        cur = self.dbHelper.getcursor()

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
          return False

        except Exception as err:
          print("General Exception from addPost():".format(err))
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

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException is raised by addPostPermission():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        except Exception as err:
          print("General Exception from addPostPermission():".format(err))
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

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException is raised by updateMessage():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        except Exception as err:
          print("General Exception is raised by updateMessage():".format(err))
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

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException is raised by updateTime():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        except Exception as err:
          print("General Exception is raised by updateTime():".format(err))
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

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException is raised by updateTime():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")

          return False

        except Exception as err:
          print("General Exception is raised by authorAuthenticate():".format(err))
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
            print("neeed to be fixed")
            #self.addUserPermission(dbhelper,pid,user)
        else:
            query = "DELETE FROM user_permission WHERE pid='%s'"%(pid)

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException is raised by updatePermission():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        except Exception as err:
          print("General Exception is raised by updatePermission():".format(err))
          return False

        return cur.rowcount>0

    def deletePostByPid(self,pid):
        """
         delete a post or server post by pid, aid
        dbhelper -- database helper
        pid -- post id
        """
        cur = self.dbHelper.getcursor()
        query = "DELETE FROM post WHERE pid = '%s'"%(pid)

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException is raised by deletePostByPid():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        except Exception as err:
          print("General Exception is raised by deletePostByPid():".format(err))
          return False

        return cur.rowcount>0

    def deletePostByAid(self,aid):
        """
        to delete a post by authorid
        aid -- author id
        dbhelper -- database helper
        """
        cur = self.dbHelper.getcursor()
        query = "DELETE FROM post WHERE aid = '%s'"%(aid)

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException is raised by deletePostByAid():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        except Exception as err:
          print("General Exception from deletePostByAid():".format(err))
          return False

        return cur.rowcount>0

    def getPostList(self,aid):
        """
        get list of post that the user by aid can browse
        aid -- author id
        """
        re = {}
        cur = self.dbHelper.getcursor()

        #get the post if it is public
        query = "SELECT * FROM post WHERE permission='public';"

        try:
          cur.execute(query)

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from getPostList():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("1st Query:",query)
          print("****************************************")
          return None

        except Exception as err:
          print("General Exception from getPostList() 1st block:".format(err))
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

            re[pid]=post.tojson()

        #get the post if aid is its author
        query = "SELECT * FROM post WHERE permission='me' and aid='%s'"%(aid)

        try:
          cur.execute(query)

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from getPostList():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("2nd Query:",query)
          print("****************************************")
          return None

        except Exception as err:
          print("General Exception from getPostList() 2nd block:".format(err))
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

            re[pid]=post.tojson()

        #get the post if aid is specifiied user
        query = "SELECT * FROM post WHERE permission = 'user' and pid IN (SELECT pid from user_permission WHERE aid='%s')"%(aid)
        try:
          cur.execute(query)

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from getPostList():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("3rd Query:",query)
          print("****************************************")
          return None

        except Exception as err:
          print("General Exception from getPostList() 3rd block:".format(err))
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

            re[pid]=post.tojson()
        #get the post if aid is the author's friend

        authorHelper = AuthorHelper(self.dbHelper)
        authorName = authorHelper.getAuthorNameByAid(aid)

        try:
          if(authorName == None):
            raise Exception('Failed to get the name by id in getPostList() function')
        except Exception as err:
          print("***************************************")
          print(err.args)
          print("***************************************")
          return None

        query = "SELECT * FROM post WHERE permission = 'friends' and aid IN  (SELECT aid from author WHERE author_name IN (SELECT name1 FROM circle WHERE name2 ='%s' ))"%(authorName)

        try:
          cur.execute(query)

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from getPostList():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("4th Query",query)
          print("****************************************")
          return None

        except Exception as err:
          print("General Exception from getPostList() 4th block:".format(err))
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

            re[pid]=post.tojson()
        #get the post if aid is the author's friends`s friend

        query = "SELECT * FROM post WHERE permission = 'fof' and aid IN  (SELECT aid from author WHERE author_name IN (SELECT name1 FROM circle WHERE name2 IN (SELECT name1 FROM circle WHERE name2 = '%s')))"%(authorName)

        try:
          cur.execute(query)

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from getPostList():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("5th Query",query)
          print("****************************************")
          return None

        except Exception as err:
          print("General Exception from getPostList() 5th block:".format(err))
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

            re[pid]=post.tojson()

        #get the post if aid is in the same host as the permission's requirement

        query = "SELECT * FROM post WHERE permission='fomh' AND aid IN (SELECT a1.aid FROM author a1,author a2 WHERE a1.sid = a2.sid AND a2.aid = '%s')"%(aid)

        try:
          cur.execute(query)

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from getPostList():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("6th Query:",query)
          print("****************************************")
          return None

        except Exception as err:
          print("General Exception from getPostList() 6th block:".format(err))
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

            re[pid]=post.tojson()
            
        cur.close() 
        return json.dumps(re)
