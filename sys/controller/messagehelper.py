from databasehelper import *
class MessageHelper:
    """ add a new message if it is unsuccessful, it returns -1
    """
    def addNewMessage(self,dbhelper,re_name,red_name):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query ="INSERT INTO message VALUES(NULL,'%s','%s','0')"%(re_name,red_name)
        cur.execute(query)
        dbhelper.commit()
        return cur.rowcount>0
    def makeMessageRead(self,debhelper,re_name,red_name):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query ="UPDATE message SET read_check = '1' WHERE request_name = '%s' and requested_name = '%s'"%(re_name,red_name)
        print query
        cur.execute(query)
