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
    '''
       add friend for the author
    '''
    def addFriendForAuthor(self,aid1,aid2):

        cur = self.dbAdapter.getcursor()
        data = [(aid1,aid2),(aid2,aid1),]
        query ="INSERT INTO circle VALUES(%s,%s)"

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
          return False

        if cur.rowcount == 2 :
          return True

        return False

    def deleteFriendOfAuthor(self,aid1,aid2):
        """
            aid1 should be the author wants to delete
            aid2 should be the author will be deleted
            """
        cur = self.dbAdapter.getcursor()
        query = ("DELETE FROM circle WHERE "
                "aid1='%s' AND aid2='%s'")%(aid1,aid2)
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
        ''' get a list of all friend by author id'''

        result = []
        cur = self.dbAdapter.getcursor()
        query = ("SELECT A.aid,A.name,A.nick_name,A.sid,A.email,A.gender,A.city,A.birthday,A.img_path "
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

        return cur.fetchall()

    def getFriendOfMyHomeServerList(self,aid):
        # DO NOT DELETE THE COMMENT
        # TODO:
        #
        # Find the all the friends that are from our server through author's aid
        #
        # [Success] Returns an jason array of author objects / empty jason array
        # [Exception Caught] return null
        cur = self.dbAdapter.getcursor()
        query = ("SELECT A.aid,A.name,A.nick_name,A.sid,A.email,A.gender,A.city,A.birthday,A.img_path "
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

        return cur.fetchall()
    '''
     get friend of friend's list
    '''
    def getFriendOfFriendList(self,aid):
        
        cur = self.dbAdapter.getcursor()
        query = ("SELECT A.aid,A.name,A.nick_name,A.sid,A.email,A.gender,A.city,A.birthday,A.img_path "
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

        return cur.fetchall()
    '''
    Determine if two authors are friends or not
    '''
    def areFriends(self,aid1,aid2):

      cur = self.dbAdapter.getcursor()
      query = ("SELECT * FROM circle WHERE aid1 ='%s' AND aid2 = '%s';")%(aid1,aid2)

      try:

        cur.execute(query)

      except mysql.connector.Error as err:
        print("****************************************")
        print("SQLException from areFriends():")
        print("Error code:", err.errno)
        print("SQLSTATE value:", err.sqlstate)
        print("Error message:", err.msg)
        print("Query:",query)
        print("****************************************")
        return None

      return len(cur.fetchall()) > 0

    '''
    Check if the authors in the list are friends of a specific author
    '''
    def areFriendsOfAuthor(self,aid1,aidsList):

      if len(aidsList) == 0:
        return None
      cur = self.dbAdapter.getcursor()
     

      #Change each aid to 'aid2 = aid' formate
      for i in range(len(aidsList)):
        aidsList[i] = ("aid2 = '%s'")%(aidsList[i])
      
      # Add 'OR' Between two aids
      aidsListQuery = ['OR'] * (len(aidsList) * 2 - 1)
      aidsListQuery[0::2] = aidsList

      query = ("SELECT aid2 FROM circle WHERE aid1 = '%s' AND (%s);")%(aid1,' '.join(aidsListQuery))
      try:

        cur.execute(query)

      except mysql.connector.Error as err:
        print("****************************************")
        print("SQLException from areFriendsOfAuthor():")
        print("Error code:", err.errno)
        print("SQLSTATE value:", err.sqlstate)
        print("Error message:", err.msg)
        print("Query:",query)
        print("****************************************")
        return None

      return cur.fetchall()






      


