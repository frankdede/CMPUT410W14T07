import mysql.connector
from databasehelper import *
import sys
import json
sys.path.append("sys/model")
from message import *
class Messagehelper:
    """ add a new message if it is unsuccessful, it returns -1
    """
    dbHelper = None
    def __init__(self,dbHelper):
        self.dbHelper = dbHelper

    def addNewMessage(self,re_name,red_name):

        cur = self.dbHelper.getcursor()
        query ="INSERT INTO message VALUES(NULL,'%s','%s','0')"%(re_name,red_name)

        try:
          cur.execute(query)
          self.dbHelper.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from addNewMessage():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        except Exception as err:
          print("General Exception from addNewMessage():".format(err))
          return False

        return cur.rowcount>0

    """
    to set message read by its primary key(re_name,red_name,time)
    """
    def setMessageRead(self,recipient,sender):

        cur = self.dbHelper.getcursor()
        query ="UPDATE message SET status = 1 WHERE recipient = '%s' and sender = '%s'"%(time,recipient,sender)
        try:
          cur.execute(query)
          self.dbHelper.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from addNewMessage():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        except Exception as err:
          print("General Exception from addNewMessage():".format(err))
          return False

        return cur.rowcount>0
    """
    get a list of message of a same requester
    """
    def getMessageListByAuthorName(self,recipient):
        re = []
        cur = self.dbHelper.getcursor()
        query ="SELECT * FROM  message  WHERE recipient = '%s'"%(recipient)

        try:
            cur.execute(query)
            for item in cur:
                re.append(Message(item[1],item[2],str(item[0]),item[3]).tojson())
            return json.dumps(re)

        except mysql.connector.Error as err:

            print("****************************************")
            print("SQLException from getMessageListByAuthorName():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return None

        except Exception as err:
            print("General Exception from getMessageListByAuthorName():".format(err))
            return None
    """
    to get a list of unread message of a requester
    """
    def getUnreadMessageListByAuthorName(self,recipient):

        cur = self.dbHelper.getcursor()
        query ="SELECT * FROM  message  WHERE status = 0 AND recipient = '%s'"%(recipient)
        try:
            cur.execute(query)
            re = []
            for item in cur:
                re.append(Message(item[1],item[2],str(item[0]),item[3]).tojson())
            return json.dumps(re)

        except mysql.connector.Error as err:

            print("****************************************")
            print("SQLException from getUnreadMessageListByAuthorName():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return None

        except Exception as err:
            print("General Exception from getUnreadMessageListByAuthorName():".format(err))
            return None
    """
    To get the number of message
    """
    def getMessageCountByAuthorName(self,recipient):

        cur = self.dbHelper.getcursor()
        query ="SELECT count(*) FROM  message  WHERE status = 0 AND recipient = '%s'"%(recipient)
        try:
            cur.execute(query)
            i = cur.fetchone()
            if i is not None:
                return i[0]
            else:
                return 0

        except mysql.connector.Error as err:

            print("****************************************")
            print("SQLException from getMessageCountByAuthorName():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return None

        except Exception as err:
            print("General Exception from getMessageCountByAuthorName():".format(err))
            return None

    def deleteAllMessageByAuthorName(self,sender):
        
        cur = self.dbHelper.getcursor()
        query = "DELETE FROM message WHERE recipient ='%s'"%(sender)
        try:
          cur.execute(query)
          self.dbHelper.commit()

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from addNewMessage():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        except Exception as err:
          print("General Exception from addNewMessage():".format(err))
          return False

        return cur.rowcount>0

