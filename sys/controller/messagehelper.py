from databasehelper import *
import sys,json
sys.path.append('../model')
from message import *
class Messagehelper:
    """ add a new message if it is unsuccessful, it returns -1
    """
    def addNewMessage(self,dbhelper,re_name,red_name):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query ="INSERT INTO message VALUES(NULL,'%s','%s','0')"%(re_name,red_name)
        print query
        cur.execute(query)
        dbhelper.commit()
        return cur.rowcount>0
    """
    to set message read by its primary key(re_name,red_name,time)
    """
    def setMessageRead(self,dbhelper,re_name,red_name,time):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query ="UPDATE message SET read_check = '1' WHERE time = '%s' and request_name = '%s' and requested_name = '%s'"%(time,re_name,red_name)
        print query
        cur.execute(query)
        dbhelper.commit()
        return cur.rowcount>0
    """
    get a list of message of a same requester
    """
    def getMessageListByAuthorName(self,dbhelper,re_name):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query ="SELECT * FROM  message  WHERE requested_name = '%s'"%(re_name)
        print query
        cur.execute(query)
        re = []
        for item in cur:
            re.append(Message(item[1],item[2],str(item[0]),item[3]).tojson())
        return json.dumps(re)
    """
    to get a list of unread message of a requester
    """
    def getUnreadMessageListByAuthorName(self,dbhelper,re_name):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query ="SELECT * FROM  message  WHERE read_check = '0' AND requested_name = '%s'"%(re_name)
        print query
        cur.execute(query)
        re = []
        for item in cur:
            re.append(Message(item[1],item[2],str(item[0]),item[3]).tojson())
        return json.dumps(re)
    """
    To get the number of message
    """
    def getMessageCountByAuthorName(self,dbhelper,re_name):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query ="SELECT count(*) FROM  message  WHERE read_check = '0' AND requested_name = '%s'"%(re_name)
        cur.execute(query)
        i = cur.fetchone()
        if i is not None:
            return i[0]
        else:
            return 0
    def deleteAllMessageByAuthorName(self,dbhelper,red_name):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query = "DELETE FROM message WHERE requested_name='%s'"%(red_name)
        cur.execute(query)
        dbhelper.commit()
        return cur.rowcount>0
if __name__ =="__main__":
    dbhelper = Databasehelper()
    mhelper = Messagehelper()
    mhelper.addNewMessage(dbhelper,"test1","admin")
    mhelper.addNewMessage(dbhelper,"test2","admin")
    a = mhelper.getMessageListByAuthorName(dbhelper,"admin")
    print a
    #print mhelper.setMessageRead(dbhelper,"test1","test2")
    print "----------------------------"
    print mhelper.getMessageCountByAuthorName(dbhelper,"admin")
    #print mhelper.deleteAllMessageByAuthorName(dbhelper,"test2")
    #print mhelper.getUnreadMessageListByAuthorName(dbhelper,"test1")
