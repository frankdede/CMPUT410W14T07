import json
from mysql.connector.errors import Error
from DatabaseAdapter import *
import Utility
import sys
sys.path.append("sys/model")
from author import *


class CircleHelper:

    dbAdapter = None

    def __init__(self,dbAdapter):
        self.dbAdapter = dbAdapter

    def addFriendForAuthor(self,aid1,aid2):

        cur = self.dbAdapter.getcursor()
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
        cur = self.dbAdapter.getcursor()
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
        cur = self.dbAdapter.getcursor()
        query = ("SELECT A.aid,A.name,A.email,A.gender,A.city,A.img_path,A.sid,A.nick_name "
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
            friend = Author(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            result.append(friend.tojson())

        return json.dumps(result)

    def getFriendOfMyHomeServerList(self,aid):
        # DO NOT DELETE THE COMMENT
        # TODO:
        #
        # Find the all the friends that are from our server through author's aid
        #
        # [Success] Returns an jason array of author objects / empty jason array
        # [Exception Caught] return null
        result = []
        cur = self.dbAdapter.getcursor()
        query = ("SELECT A.aid,A.name,A.email,A.gender,A.city,A.img_path,A.sid,A.nick_name "
                 "FROM author A "
                 "WHERE A.aid in (SELECT C.aid2 FROM circle C WHERE C.aid1='%s') AND sid = 1")%(aid)
        try:
          cur.execute(query);

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from getFriendOfMyHomeServerList():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Query:",query)
          print("****************************************")
          return None

        for row in cur:
            friend = Author(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            result.append(friend.tojson())

        return json.dumps(result)

    def getFriendOfFriendList(self,aid):
        result = []
        cur = self.dbAdapter.getcursor()
        query = ("SELECT A.aid,A.name,A.email,A.gender,A.city,A.img_path,A.sid,A.nick_name "
                 "FROM author A WHERE A.aid IN "
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
          return None

        result = []
        for row in cur:
            friend = Author(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            result.append(friend.tojson())

        return json.dumps(result)
