from mysql.connector.errors import Error
from databasehelper import *
import utility
import json

class AuthorHelper:
    """
    If the username and password are correct, it will return True otherwise false
    """
    dbHelper = None
    def __init__(self,dbHelper):
        self.dbHelper = dbHelper

    def authorAuthenticate(self,authorName,password):

        cur = self.dbHelper.getcursor()
        #Refactored: Author_name is changed to name
        query = "SELECT * FROM author WHERE name='%s' AND pwd='%s' AND sid=1"%(authorName,password)
        
        try:
            cur.execute(query)
            if cur.fetchone() is None:
                cur.close()
                return False
            else:
                cur.close()
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

    def getAuthorObjectByAid(self,aid):
        # DO NOT DELETE THE COMMENT
        # TODO:
        # [Success] return an jason author object
        # [Exception] return null
        # [Failed] return null
        cur = self.dbHelper.getcursor()
        query = "SELECT * FROM author WHERE aid = '%s'"%(aid)
        try:
            cur.execute(query)
            row = cur.fetchone()
            cur.close()
            if row is None:
               return None

            else:
               objects_list = []
               author = Author(row[0],row[1],row[2],row[4],row[5],row[6],row[7],row[8],row[9])
               objects_list.append(author.tojson())
               j = json.dumps(objects_list)
               return j
 
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from getAuthorObjectByAid():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return None

    def getAllAuthorObjectsForLocalServer(self):
        # DO NOT DELETE THE COMMENT
        # TODO:
        # [SUCCESS] return an array of author objects for local server
        # e.g. {{'aid':xxxxx,'name':xxxxxxx ...},{'aid':xxxxx,'name':xxxxxxx..}}
        # [Exception] return null
        # [Failed] return null
        cur = self.dbHelper.getcursor()
        query = "SELECT * FROM author WHERE sid = 1"
        try:
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            if rows is None:
               return None

            else:
               objects_list = []
               for row in rows:
                   author = Author(row[0],row[1],row[2],row[4],row[5],row[6],row[7],row[8],row[9])
                   objects_list.append(author.tojson())
               j = json.dumps(objects_list)
               return j
 
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from getAllAuthorObjectsForLocalServer():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return None

    def getAllAuthorObjectsForRemoteServer(self):
        # DO NOT DELETE THE COMMENT
        # TODO:
        # [SUCCESS] return an json array of author objects for remote server
        # e.g. {{'aid':xxxxx,'name':xxxxxxx ...},{'aid':xxxxx,'name':xxxxxxx..}}
        # [Exception] return null
        # [Failed] return null
        cur = self.dbHelper.getcursor()
        query = "SELECT * FROM author WHERE sid != 1"
        try:
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            if rows is None:
               return None

            else:
               objects_list = []
               for row in rows:
                   author = Author(row[0],row[1],row[2],row[4],row[5],row[6],row[7],row[8],row[9])
                   objects_list.append(author.tojson())
               j = json.dumps(objects_list)
               return j
 
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from getAllAuthorObjectsForLocalServer():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return None

    def addRemoteAuthor(self,authorName,sid):
        # DO NOT DELETE THE COMMENT
        # TODO:
        # [Success] return {'aid':xxxxx } (jason type)
        # [Exception] return false
        # [Failed] return false
        aid = utility.getid()
        password = ""
        nickName = ""
        query = ("INSERT INTO author(aid,name,nick_name,pwd,sid) "
                 "VALUES('%s','%s','%s','%s',%s)")%(aid,authorName,nickName,password,sid)
        try:
            cur.execute(query)

        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from addRemoteAuthor():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return False
        if cur.rowcount > 0:
            cur.close()
            return json.dumps({"aid":aid})

        cur.close()
        return False
    def updateAuthorInfo(self,aid,email,gender,city,birthday,img_path):
        # DO NOT DELETE THE COMMENT
        # TODO:
        # [Success] return true
        # [Exception] return false
        # [Failed] return false
        query = "UPDATE author SET email = '%s', gender = '%s',city = '%s',birthday = '%s', img_path = '%s' WHERE aid = '%s'"%(email,gender,city,birthday,img_path,aid)
        try:
            cur.execute(query)
            return True
        except mysql.connector.Error as err:
            print("****************************************")
            print("updateAuthorInfo():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return False

    def updateNickNameByAid(self,aid,newNickName):

        cur = self.dbHelper.getcursor()
        query = "UPDATE author SET nick_name = '%s' WHERE aid = '%s'"%(newNickName,aid)
        
        try:
          cur.execute(query)
          # Auto-commit
          #self.dbHelper.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from updateNickNameByAid():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        return cur.rowcount>0

    def updatePasswordByAid(self,aid,newPassword):

        cur = self.dbHelper.getcursor()
        query = "UPDATE author SET pwd = '%s' WHERE aid='%s'"%(newPassword,aid)

        try:
          cur.execute(query)
          # Auto-commit
          #self.dbHelper.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from updatePasswordByUserId():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        return cur.rowcount>0

    # to add an author to database the server_id is defualtly 1 if server_id is not provided

    def deleteAuthor(self,aid):

        cur = self.dbHelper.getcursor()

        query = ("DELETE FROM author "
                 "WHERE aid = '%s'") %(aid)
        
        try:
          cur.execute(query)
          # Auto-commit
          #self.dbHelper.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from deleteAuthor():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        return cur.rowcount>0

    def addAuthor(self,authorName,password,nickName,sid=1):

        cur = self.dbHelper.getcursor()
        aid =utility.getid()

        query = ("INSERT INTO author(aid,name,nick_name,pwd,sid) "
                 "VALUES('%s','%s','%s','%s',%s)")%(aid,authorName,nickName,password,sid)
       
        try:
          cur.execute(query)

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from addAuthor():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        if cur.rowcount > 0:

            return json.dumps({"aid":aid})

        return False
