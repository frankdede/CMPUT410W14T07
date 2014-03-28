import json
from mysql.connector.errors import Error
from DatabaseAdapter import *
import Utility
import sys
sys.path.append("sys/model")
from image import *
class ImageHelper:
    dbAdapter = None
    def __init__(self,dbAdapter):
        self.dbAdapter = dbAdapter
    def getImageByAid(self,aid):
        cur = self.dbAdapter.getcursor()
        query = "SELECT * FROM image WHERE aid ='%s'"%(aid)
        try:
            cur.execute(query)
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from addNewCircle():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Query:",query)
            print("****************************************")
            return False
        re = []
        if cur is not None:
            for row in cur:
                re.append(Image(row[0],row[2],row[1],row[3],row[4]))
            return re
        else:
            return None
    def getImageByPid(self,pid):
        cur = self.dbAdapter.getcursor()
        query = "SELECT * FROM image WHERE pid ='%s'"%(pid)
        try:
            cur.execute(query)
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from addNewCircle():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Query:",query)
            print("****************************************")
            return False
        re = []
        if cur is not None:
            for row in cur:
                re.append(Image(row[0],row[2],row[1],row[3],row[4]))
            return re
        else:
            return None
    def insertImage(self,path,aid,pid):
        cur = self.dbAdapter.getcursor()
        iid = Utility.getid()
        query = "INSERT INTO image VALUES('%s',NULL,'%s','%s','%s')"%(iid,path,aid,pid)
        try:
            cur.execute(query)
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from addNewCircle():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Query:",query)
            print("****************************************")
            return False
        return iid
    def deleteImageByAid(self,aid):
        cur = self.dbAdapter.getcursor()
        query = "DELETE FROM image WHERE aid ='%s'"%(aid)
        try:
            cur.execute(query)
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from addNewCircle():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Query:",query)
            print("****************************************")
            return False
        return cur.rowcount>0
    def deleteImageByPid(self,pid):
        cur = self.dbAdapter.getcursor()
        query = "DELETE FROM image WHERE pid ='%s'"%(pid)
        try:
            cur.execute(query)
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from addNewCircle():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Query:",query)
            print("****************************************")
            return False
        return cur.rowcount>0
    def deleteImageByImageId(self,iid):
        cur = self.dbAdapter.getcursor()
        query = "DELETE FROM image WHERE image_id ='%s'"%(iid)
        try:
            cur.execute(query)
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from addNewCircle():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Query:",query)
            print("****************************************")
            return False
        return cur.rowcount>0
