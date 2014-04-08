import json
from mysql.connector.errors import Error
from DatabaseAdapter import *
import Utility

class ServerHelper:

    def __init__(self,dbAdapter):
        self.dbAdapter = dbAdapter

    def doesServerExists(self,url):
        cur = self.dbAdapter.getcursor()
        query = ("SELECT sid FROM servers WHERE url = '%s';")%(url)
        try:
            cur.execute(query)
        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from doesServerExists():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Query:",query)
          print("****************************************")
          return False
      
        result = cur.fetchone()
        if(result != None):
          return result[0]
        else:
          return False


    def addServer(self,name,url,local):
        cur = self.dbAdapter.getcursor()
        sid =Utility.getid()
        query = ("INSERT INTO servers VALUES('%s','%s','%s',%s)")%(sid,name,url,local)
        try:
            cur.execute(query)
        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from doesServerExists():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Query:",query)
          print("****************************************")
          return None

        if cur.rowcount > 0:
          return sid
        else:
          return False

    def getServerNameBySid(self,sid):
        cur = self.dbAdapter.getcursor()
        query = "SELECT name FROM servers WHERE sid='%s'"%(sid)
        try:
            cur.execute(query)
        except Exception, e:
          print("****************************************")
          print("SQLException from getServerNameBySid():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Query:",query)
          print("****************************************")
          return None

        re = cur.fetchone()

        if (re != None):
          if(len(re) != 0):
            return re[0]
        return None

    def getServerUrlBySid(self,sid):
        cur = self.dbAdapter.getcursor()
        query = "SELECT url FROM servers WHERE sid='%s'"%(sid)
        try:
          cur.execute(query)
        except Exception, e:
          print("****************************************")
          print("SQLException from getServerUrlBySide():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Query:",query)
          print("****************************************")
          return None

        re = cur.fetchone()
        
        if (re != None):
          if(len(re) != 0):
            return re[0]
        return None
