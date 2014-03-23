import mysql.connector
from DatabaseAdapter import *
import sys
import json

class RequestHelper:

    dbHelper = None
    def __init__(self,dbHelper):
        self.dbHelper = dbHelper

    def addNewRequest(self,recipientId,senderId):

        
        query ="INSERT INTO request VALUES(NULL,'%s','%s')"%(recipientId,senderId)

        cur = self.dbHelper.getcursor()
        try:
          cur.execute(query)

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from addNewRequest():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return None

        if cur.rowcount>0:

          return json.dumps({'recipient_id':recipientId,'sender_id':senderId})

        else:

          return None

    """
    Delete a request based on recipientId and senderId

    """
        
    def deleteRequest(self,recipientId,senderId):

        cur = self.dbHelper.getcursor()
        query =("DELETE FROM request "
                "WHERE recipient_id = '%s' AND sender_id = '%s'")%(recipientId,senderId)
        try:
          cur.execute(query)

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from deleteRequest():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False
          
        return cur.rowcount>0

    """
    get a list of message of a same recipient
    """
    def getRequestListByAid(self,recipientId):
        result = []
        cur = self.dbHelper.getcursor()

        query =("SELECT sender_id,time "
               "FROM request WHERE recipient_id = '%s'")%(recipientId)

        try:
            cur.execute(query)
          
        except mysql.connector.Error as err:

            print("****************************************")
            print("SQLException from getMessageListByAuthorName():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return None

        for row in cur:
                result.append({'sender_id':row[0],'time':str(row[1])})

        return json.dumps(result)

    """
    To get the number of requests
    """
    def getRequestCountByAid(self,recipientId):

        cur = self.dbHelper.getcursor()

        query = ("SELECT count(*) FROM request "
                 "WHERE recipient_id = '%s'")%(recipientId)
        try:
            cur.execute(query)
            row = cur.fetchone()

        except mysql.connector.Error as err:

            print("****************************************")
            print("SQLException from getRequestCountByAid():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return None

        
        if row != None:
            return json.dumps({'count':row[0]})
        else:
            return json.dumps({'count':0})

    def deleteAllRequestByAid(self,recipient_id):
        
        cur = self.dbHelper.getcursor()
        query = "DELETE FROM request WHERE recipient_id ='%s'"%(recipient_id)

        try:
          cur.execute(query)

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from deleteAllRequestByAid():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        return cur.rowcount>0

