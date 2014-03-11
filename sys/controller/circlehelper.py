from databasehelper import*
class CircleHelper:
    """ add a new friend because the relationship is unique. If the relationship is already existed
it returns -1
    """
    dbHelper = None
    def __init__(self,dbHelper):
        self.dbHelper = dbHelper

    def addNewCircle(self,name1,name2,sid=1):

        cur = self.dbHelper.getcursor()
        query = "SELECT * FROM circle WHERE name1='%s' AND name2='%s' AND sid=%d"%(name1,name2,sid)
        try:
          cur.execute(query)

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from addNewCircle():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        except Exception as err:
          print("General Exception from addNewCircle():".format(err))
          return False

        if cur.fetchone() is None:
            query ="INSERT INTO circle VALUES('%s','%s',%d)"%(name1,name2,sid)
            try:
                cur.execute(query)
                self.dbHelper.commit()

            except mysql.connector.Error as err:

                print("****************************************")
                print("SQLException from addNewCircle():")
                print("Error code:", err.errno)
                print("SQLSTATE value:", err.sqlstate)
                print("Error message:", err.msg)
                print("Might be query issue:",query)
                print("****************************************")
                return False

            except Exception as err:
                print("General Exception from addPost():".format(err))
                return False

            return cur.rowcount>0
        else:
            return False

    def deleteCircle(self,name1,name2):

        cur = self.dbHelper.getcursor()
        query = "DELETE FROM circle WHERE name1='%s' AND name2='%s' AND sid=1"%(name1,name2)
        try:
            cur.execute(query)
            self.dbHelper.commit()

        except mysql.connector.Error as err:

            print("****************************************")
            print("SQLException from deleteCircle():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return False

        except Exception as err:
            print("General Exception from deleteCircle():".format(err))
            return False

        return cur.rowcount>0

#remove  author's all friends 
    def removeCircle(self,name1):
        
        cur = self.dbHelper.getcursor()
        query = "DELETE FROM circle WHERE name1='%s' AND sid=1"%(name1)
        try:
            cur.execute(query)
            self.dbHelper.commit()

        except mysql.connector.Error as err:

            print("****************************************")
            print("SQLException from deleteCircle():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return False

        except Exception as err:
            print("General Exception from deleteCircle():".format(err))
            return False

        return cur.rowcount>0

#get friend list of a author
    def getFriendList(self,name1,sid=1):

        cur = self.dbHelper.getcursor()
        query = "SELECT name2 FROM circle WHERE name1='%s' AND sid='%d'"%(name1,sid)
        try:
          cur.execute(query);

        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from getFriendList():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return None

        except Exception as err:
          print("General Exception from getFriendList():".format(err))
          return None

        re = []
        for fid in cur:
            re.append(fid[0])
        cur.close()
        return re

#get list of friend of friends
    def getFriendOfFriend(self,name1,sid=1):

        cur = self.dbHelper.getcursor()
        query = "SELECT name2 FROM circle WHERE name1 in (SELECT name2 FROM circle WHERE name1='%s' AND sid='%d')"%(name1,sid)
        try:
          cur.execute(query)
          
        except mysql.connector.Error as err:

          print("****************************************")
          print("SQLException from getFriendOfFriend():")
          print("Error code:", err.errno)
          print("SQLSTATE value:", err.sqlstate)
          print("Error message:", err.msg)
          print("Might be query issue:",query)
          print("****************************************")
          return False

        except Exception as err:
          print("General Exception from getFriendOfFriend():".format(err))
          return False
        re = []
        for fid in cur:
            re.append(fid[0])
        return re
