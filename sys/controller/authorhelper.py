from mysql.connector.errors import Error
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
        query = "SELECT * FROM author WHERE author_name='%s' AND pwd='%s' AND sid=1"%(authorName,password)
        
        try:
            cur.execute(query)
            if cur.fetchone() is None:
                return False
            else:
                return True

        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from authorAuthenticate():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return False

        except Exception as err:
            print("General Exception from authorAuthenticate():".format(err))
            print
            return False
    """
    to check the author whether is existed
    """
    def doesAuthorExist(self,authorName):

        cur = self.dbHelper.getcursor()
        query = "SELECT * FROM author WHERE author_name='%s' AND sid=1"%authorName

        try:
            cur.execute(query)
            if cur.fetchone() is None:
                return False
            else:
                return True
        except mysql.connector.Error as err:

            print("****************************************")
            print("SQLException from doesAuthorExist():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return False

        except Exception as err:
            print("General Exception from doesAuthorExist():".format(err))
            return False

    def getAidByAuthorName(self,authorName):

        cur = self.dbHelper.getcursor()
        query = "SELECT aid FROM author WHERE author_name='%s' AND sid=1"%authorName

        try:
            cur.execute(query)
            first = cur.fetchone()
            if first is None:
                return first
            else:
                return first[0]

        except mysql.connector.Error as err:

            print("****************************************")
            print("SQLException from getAidByAuthorName():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            print("Might be query issue",query)
            return False

        except Exception as err:
            print("General Exception from getAidByAuthorName():".format(err))

    def getNameByAid(self,aid):

        cur = self.dbHelper.getcursor()
        query = "SELECT author_name FROM author WHERE aid='%s' AND sid=1"%aid
        try:
            cur.execute(query)
            first = cur.fetchone()
            if first is None:
                return first
            else:
                return first[0]

        except mysql.connector.Error as err:

            print("****************************************")
            print("SQLException from getNameByAid():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return False

        except Exception as err:

            print("General Exception from getNameByAid():".format(err))

    def updateNickNameByUserId(self,userId,newNickName):

        cur = self.dbHelper.getcursor()
        query = "UPDATE author SET pwd = '%s' WHERE nick_name='%s'"%(newNickName,userId)
        
        try:
          cur.execute(query)
          self.dbHelper.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from updateNickNameByUserId():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        except Exception as err:
            print("General Exception from updateNickNameByUserId():".format(err))

        return cur.rowcount>0

        

    def updatePasswordByUserId(self,userId,newPassword):

        cur = self.dbHelper.getcursor()
        query = "UPDATE author SET pwd = '%s' WHERE aid='%s'"%(newPassword,user_id)

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from updatePasswordByUserId():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        except Exception as err:
            print("General Exception from updatePasswordByUserId():".format(err))

        return cur.rowcount>0

    # to add an author to database the server_id is defualtly 1 if server_id is not provided
    def deleteAuthor(self,authorName,serverId=1):

        cur = self.dbHelper.getcursor()

        if self.doesAuthorExist(authorName) is False:
            return False

        query = "DELETE FROM author WHERE author_name = '%s'"%authorName
        ##print query
        try:
          cur.execute(query)
          self.dbHelper.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from deleteAuthor():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        except Exception as err:
            print("General Exception from deleteAuthor():".format(err))

        return cur.rowcount>0

    def addAuthor(self,authorName,password,nickName,serverId=1):

        cur = self.dbHelper.getcursor()

        if self.doesAuthorExist(authorName) is True:

            return False

        userId =utility.getid()
        query = "INSERT INTO author VALUES('%s','%s','%s',%s,'%s')"%(userId,authorName,password,serverId,nickName)
        ##print query
        try:
          cur.execute(query)
          self.dbHelper.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from addAuthor():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        except Exception as err:
            print("General Exception from addAuthor():".format(err))

        return cur.rowcount>0
