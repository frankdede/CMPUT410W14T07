from databasehelper import*
class CircleHelper:
    """ add a new friend because the relationship is unique. If the relationship is already existed
it returns -1
    """
    def addnewcircle(self,dbhelper,name1,name2,sid=1):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query = "SELECT * FROM circle WHERE name1='%s' AND name2='%s' AND sid=%d"%(name1,name2,sid)
        print query
        cur.execute(query)
        if cur.fetchone() is None:
            query ="INSERT INTO circle VALUES('%s','%s',%d)"%(name1,name2,sid)
            cur.execute(query)
            dbhelper.commit()
        else:
            return -1
    def deletecircle(self,dbhelper,name1,name2):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query = "DELETE FROM circle WHERE name1=%s AND name2=%s AND sid=1"
        cur.execute(query,(name1,name2))
        dbhelper.commit()
    def getfriendlist(self,dbhelper,name1,sid=1):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query = "SELECT name2 FROM circle WHERE name1='%s' AND sid='%d'"%(name1,sid)
        cur.execute(query)
        re = []
        for fid in cur:
            re.append(fid[0])
        return re
    def getfriendoffriend(self,dbhelper,name1,sid=1):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query = "SELECT name2 FROM circle WHERE name1 in (SELECT name2 FROM circle WHERE name1='%s' AND sid='%d')"%(name1,sid)
        cur.execute(query)
        re = []
        for fid in cur:
            re.append(fid[0])
        return re
if __name__ == '__main__':
    from authorhelper import *
    dbhelper = Databasehelper()
    authorhelper = AuthorHelper()
   # authorhelper.addauthor(dbhelper,"test1","123","123")
   # authorhelper.addauthor(dbhelper,"test3","123","123")
    circlehelper = CircleHelper()
    circlehelper.addnewcircle(dbhelper,"test1","test2")
    circlehelper.addnewcircle(dbhelper,"test1","test3")
    circlehelper.addnewcircle(dbhelper,"test2","test3")
    li = circlehelper.getfriendlist(dbhelper,"test1")
    print li
    li =circlehelper.getfriendoffriend(dbhelper,"test1")
    print li
