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
        query = "SELECT * FROM circle WHERE aid=%s AND fid=%s AND sid=%d"
        cur.execute(query,(name1,name2,sid))
        if cur.fetchnone() is None:
            query ="INSERT INTO circle VALUES(%s,%s,%d)"
            cur.execute(query,(name1,name2,sid))
        else:
            return -1
if __name__ == '__main__':
    dbhelper = Databasehelper()
    circlehelper = CircleHelper()
    circlehelper.addnewcircle(dbhelper,"Admin","Admin","1")
