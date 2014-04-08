from mysql.connector.errors import Error
from DatabaseAdapter import *
import sys
sys.path.append("sys/model")
import Utility
import json

class PostPermissionHelper:
    def __init__(self,dbAdapter):
        self.dbAdapter = dbAdapter
   
    def addPostPermission(self,pid,aidsList):
    '''add post permisstion to post'''

        cur = self.dbAdapter.getcursor()

        if len(aidsList) == 0:
          return False

        data = []
        for aid in aidsList:
            data.append(tuple([pid,aid]))

        query = "INSERT INTO post_permission VALUES(%s,%s)"

        try:
          cur.executemany(query,data)

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException is raised by addPostPermission():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        return cur.rowcount>0
        
