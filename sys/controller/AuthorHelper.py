from mysql.connector.errors import Error
from DatabaseAdapter import *
import sys
sys.path.append("sys/model")
from author import *
import Utility
import json

class AuthorHelper:
    """
    If the username and password are correct, it will return True otherwise false
    """
    def __init__(self,dbAdapter):
        self.dbAdapter = dbAdapter

    def authorAuthenticate(self,authorName,password):

        cur = self.dbAdapter.getcursor()
        #Refactored: Author_name is changed to name
        query = "SELECT * FROM author WHERE name='%s' AND pwd='%s' AND sid=1"%(authorName,password)
        
        try:
            cur.execute(query)
            row = cur.fetchone()
            if  row is None:
                cur.close()
                return False
            else:
                re_aid =""
                re_aid = row[0]
                cur.close()
                return json.dumps({"aid":re_aid})

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
        cur = self.dbAdapter.getcursor()
        query = "SELECT aid,name,nick_name,sid,email,gender,city,birthday,img_path FROM author WHERE aid='%s'"%(aid)
        try:
            cur.execute(query)
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from getFriendOfFriend():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Query:",query)
            print("****************************************")
            return None
        row = cur.fetchone()
        if row is None:
            return None
        else:
            friend = Author(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
            return friend

    def getAllAuthorObjectsForLocalServer(self):
        """
        DO NOT DELETE THE COMMENT
         TODO:
         [SUCCESS] return an array of author objects for local server
         e.g. {{'aid':xxxxx,'name':xxxxxxx ...},{'aid':xxxxx,'name':xxxxxxx..}}
         [Exception] return null
         [Failed] return null
        """
        result = []
        cur = self.dbAdapter.getcursor()
        query = ("SELECT aid,name,nick_name,sid,email,gender,city,birthday,img_path from author WHERE sid = 1")
        try:
            cur.execute(query)
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from getFriendOfFriend():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Query:",query)
            print("****************************************")
            return None
        result = []
        for row in cur:
            friend = Author(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
            result.append(friend)
        return result

    def getAllAuthorObjectsForRemoteServer(self):
        # DO NOT DELETE THE COMMENT
        # TODO:
        # [SUCCESS] return an json array of author objects for remote server
        # e.g. {{'aid':xxxxx,'name':xxxxxxx ...},{'aid':xxxxx,'name':xxxxxxx..}}
        # [Exception] return null
        # [Failed] return null
        result = []
        cur = self.dbAdapter.getcursor()
        query = ("SELECT aid,name,email,gender,city,img_path,sid,nick_name from author WHERE sid != 1")
        try:
            cur.execute(query)
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from getFriendOfFriend():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Query:",query)
            print("****************************************")
            return None
        for row in cur:
            author = Author(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            result.append(author)
        return result

    def addLocalAuthor(self,authorName,nickName,password):
        # DO NOT DELETE THE COMMENT 
        # TODO:
        # [Success] return {'aid':xxxxx } (jason type)
        # [Exception Caught] return false
        # [Failed] return false
        cur = self.dbAdapter.getcursor()
        import utility
        aid = utility.getid()
        query = ("INSERT INTO author values('%s','%s','%s','%s',1,'','','','','')"%(aid,authorname,nickname,password))
        try:
            cur.execute(query)
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from getFriendOfFriend():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Query:",query)
            print("******************************")
            return None
            
        return json.dumps({'aid',aid})

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

        cur = self.dbAdapter.getcursor()
        query = "UPDATE author SET nick_name = '%s' WHERE aid = '%s'"%(newNickName,aid)
        
        try:
          cur.execute(query)

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

        cur = self.dbAdapter.getcursor()
        query = "UPDATE author SET pwd = '%s' WHERE aid='%s'"%(newPassword,aid)

        try:
          cur.execute(query)

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

        cur = self.dbAdapter.getcursor()

        query = ("DELETE FROM author "
                 "WHERE aid = '%s'") %(aid)
        
        try:
          cur.execute(query)

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

        cur = self.dbAdapter.getcursor()
        aid =Utility.getid()

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
        return json.dumps({"aid":aid})
    def getRecommendedAuthorList(self,aid):
        cur = self.dbAdapter.getcursor()
        query = ("SELECT c2.aid2,a.name ,count(*)as num FROM circle c1,circle c2,author a WHERE c1.aid2 = c2.aid1 and c1.aid1 !=c2.aid2 and c1.aid1 ='%s' and a.aid=c2.aid2 group by c1.aid1,c2.aid2 order by num desc;")%(aid)
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
        re = []
        for row in cur:
            re.append({"aid":row[0],"name":row[1]})
        return re
