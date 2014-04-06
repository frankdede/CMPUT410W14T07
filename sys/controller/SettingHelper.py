import json
from mysql.connector.errors import Error
from DatabaseAdapter import *
import Utility
import sys
sys.path.append("sys/model")
class SettingHelper:
    dbAdapter = None
    def __init__(self,dbAdapter):
        self.dbAdapter = dbAdapter
    def addSignUpRestriction(self):
        cur = self.dbAdapter.getcursor()
        query = "UPDATE setting SET value = true WHERE name='SIGNUP_RESTRICTION';"
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
    def addRemotePostAccessRestriction(self):
        cur = self.dbAdapter.getcursor()
        query = "UPDATE setting SET value = true WHERE name='POST_REMOTE_ACCESS_RESTRICTION';"
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
    def addRemoteImageAccessRestriction(self):
        cur = self.dbAdapter.getcursor()
        query = "UPDATE setting SET value = true WHERE name='IMAGE_REMOTE_ACCESS_RESTRICTION';"
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
    def removeSignUpRestriction(self):
        cur = self.dbAdapter.getcursor()
        query = "UPDATE setting SET value = false WHERE name='SIGNUP_RESTRICTION';"
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
    def removeRemotePostAccessRestriction(self):
        cur = self.dbAdapter.getcursor()
        query = "UPDATE setting SET value = false WHERE name='POST_REMOTE_ACCESS_RESTRICTION';"
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
    def removeRemoteImageAccessRestriction(self):
        cur = self.dbAdapter.getcursor()
        query = "UPDATE setting SET value = false WHERE name='IMAGE_REMOTE_ACCESS_RESTRICTION';"
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
    def getSignUpRestrictionValue(self):
        cur = self.dbAdapter.getcursor()
        query = "SELECT value FROM setting WHERE name='SIGNUP_RESTRICTION';"
        try:
            cur.execute(query)
            row = cur.fetchone()
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from updatePasswordByUserId():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return False
        if row != None:
            return row[0]
        return None
    def getRemotePostAccessRestrictionValue(self):
        cur = self.dbAdapter.getcursor()
        query = "SELECT value FROM setting WHERE name='POST_REMOTE_ACCESS_RESTRICTION';"
        try:
            cur.execute(query)
            row = cur.fetchone()
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from updatePasswordByUserId():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return False
        if row != None:
            return row[0]
        return None
    def getRemoteImageAccessRestrictionValue(self):
        cur = self.dbAdapter.getcursor()
        query = "SELECT value FROM setting WHERE name='IMAGE_REMOTE_ACCESS_RESTRICTION';"
        try:
            cur.execute(query)
            row = cur.fetchone()
        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from updatePasswordByUserId():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return False
        if row != None:
            return row[0]
        return None