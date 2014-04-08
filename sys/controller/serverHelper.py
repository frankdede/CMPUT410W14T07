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
          return None

        return cur.fetchone() > 0

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

