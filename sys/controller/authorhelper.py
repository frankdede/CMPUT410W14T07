from databasehelper import *
import utility
class AuthorHelper:
    """
    If the username and password are correct, it will return True otherwise false
    """
    dbHelper = None;
    def __init__(self,dbHelper):
        self.dbHelper = dbHelper

    def authorAuthenticate(self,authorName,password):

        cur = self.dbHelper.getcursor()
        query = "SELECT * FROM author WHERE author_name=%s AND pwd=%s AND sid=1"
        cur.execute(query,(autherName,password))
        if cur.fetchone() is None:
            return False
        else:
            return True
    """
    to check the author whether is existed
    """
    def doesAuthorExist(self,authorName):

        cur = self.dbHelper.getcursor()
        query = "SELECT * FROM author WHERE author_name='%s' AND sid=1"%authorName
        cur.execute(query)
        if cur.fetchone() is None:
            return False
        else:
            return True

    def getAidByAuthorName(self,authorName):

        cur = self.dbHelper.getcursor()
        query = "SELECT aid FROM author WHERE author_name='%s' AND sid=1"%authorName
        cur.execute(query)
        first = cur.fetchone()
        if first is None:
            return first
        else:
            return first[0]

    def getNameByAid(self,aid):

        cur = self.dbHelper.getcursor()
        query = "SELECT author_name FROM author WHERE aid='%s' AND sid=1"%aid
        cur.execute(query)
        first = cur.fetchone()
        if first is None:
            return first
        else:
            return first[0]

    def updateNickNameByUserId(self,userId,newNickName):

        cur = self.dbHelper.getcursor()
        query = "UPDATE author SET pwd = '%s' WHERE nick_name='%s'"%(newNickName,userId)
        result = cur.execute(query)
        dbhelper.commit()
        return cur.rowcount>0

    def updatePasswordByUserId(self,userId,newPassword):

        cur = self.dbHelper.getcursor()
        query = "UPDATE author SET pwd = '%s' WHERE aid='%s'"%(newPassword,user_id)
        ##print query
        result = cur.execute(query)
        dbhelper.commit()
        return cur.rowcount>0

    # to add an author to database the server_id is defualtly 1 if server_id is not provided
    def deleteAuthor(self,authorName,serverId=1):

        cur = self.dbHelper.getcursor()

        if self.doesAuthorExist(authorName) is False:
            return False

        query = "DELETE FROM author WHERE author_name = '%s'"%authorName
        ##print query
        cur.execute(query)
        dbhelper.commit()
        return cur.rowcount>0

    def addAuthor(self,authorName,password,nickName,serverId=1):

        cur = self.dbHelper.getcursor()

        if self.doesAuthorExist(authorName) is True:

            return False

        user_id =utility.getid()
        query = "INSERT INTO author VALUES('%s','%s','%s',%s,'%s')"%(user_id,username,pwd,server_id,nick_name)
        ##print query
        cur.execute(query)
        dbhelper.commit()
        return cur.rowcount>0
