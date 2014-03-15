from mysql.connector.errors import Error
from databasehelper import *
import utility
import sys
sys.path.append("sys/model")
from post import *
import json

class CircleHelper:

    dbHelper = None

    def __init__(self,dbHelper):
        self.dbHelper = dbHelper

    def addFriendForAuthor(self,aid1,aid2):

        cur = self.dbHelper.getcursor()
        data = [(aid1,aid2),(aid2,aid1)]
        query ="INSERT INTO circle VALUES('%s','%s')"

        try:
          cur.executemany(query,data)

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from addNewCircle():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Query:",query)
          print("****************************************")
          return None

        if cur.rowcount == 2 :
          return json.dumps({'aid1':aid1,'aid2':aid2})
        else:
          return False;

    def deleteFriendOfAuthor(self,aid1,aid2):
        # No matter how you pass aid1 and aid2 ,this function will delete it for you
        cur = self.dbHelper.getcursor()
        query = ("DELETE FROM circle WHERE "
                "(aid1='%s' AND aid2='%s') OR (aid1='%s' AND aid2='%s')")%(aid1,aid2,aid2,aid1)
        try:
            cur.execute(query)

        except mysql.connector.Error as err:

            print("****************************************")
            print("SQLException from deleteCircle():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Query:",query)
            print("****************************************")
            return False

        return cur.rowcount>0

    def getFriendList(self,aid):

        result = []
        cur = self.dbHelper.getcursor()
        query = ("SELECT A.aid,A.name,A.email,A.city,A.img_path,A.sid,A.nick_name"
                 "FROM author A "
                 "WHERE A.aid in "
                 "(SELECT C.aid2 FROM circle C WHERE C.aid1='%s')")%(aid)
        try:
          cur.execute(query);

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from getFriendList():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Query:",query)
          print("****************************************")
          return None

        for row in cur:
            friend = Author(row[0],row[1],row[2],row[3],row.img[4],row[5],row[6])
            result.append(friend.tojson())

        return json.dumps(reuslt)


    def getFriendOfFriendList(self,aid):
        result = []
        cur = self.dbHelper.getcursor()
        query = ("SELECT A.aid,A.name,A.nick_name,A.email,A.city,A.img_path FROM author A WHERE A.aid IN "
                 "(SELECT C2.aid2 FROM circle C2 WHERE C2.aid2 <>'%s' AND C2.aid1 IN "
                 "(SELECT C1.aid2 FROM circle C1 WHERE C1.aid1 = '%s'))")%(aid,aid)
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
          return False

        result = []
        for row in cur:
            friend = Author(row[0],row[1],row[2],row[3],row.img[4],row[5],row[6])
            result.append(friend.tojson())

        return json.dumps(reuslt)
