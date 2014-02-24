from databasehelper import *
class AuthorHelper:
    """
    If the username and password are correct, it will return True otherwise fals
    """
    def authorauthenticate(self,dbhelper,username,pwd):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query = "SELECT * FROM author WHERE author_name=%s AND pwd=%s AND sid=1"
        cur.execute(query,(username,pwd))
        if cur.fetchone() is None:
            return False
        else:
            return True
    """
    to check the author whether is existed
    """
    def checkauthorexist(self,dbhelper,username):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query = "SELECT * FROM author WHERE author_name='%s' AND sid=1"%username
        cur.execute(query)
        if cur.fetchone() is None:
            return False
        else:
            return True
    def getaidbyname(self,dbhelper,username):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query = "SELECT aid FROM author WHERE author_name='%s' AND sid=1"%username
        cur.execute(query)
        first = cur.fetchone()
        if first is None:
            return first
        else:
            return first[0]
    def getnamebyaid(self,dbhelper,aid):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query = "SELECT author_name FROM author WHERE aid='%s' AND sid=1"%aid
        cur.execute(query)
        first = cur.fetchone()
        if first is None:
            return first
        else:
            return first[0]
    # to add an author to database the server_id is defualtly 1 if server_id is not provided
    def deleteauthor(self,dbhelper,username,server_id=1):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        if self.checkauthorexist(dbhelper,username) is False:
            return -1;
        cur = dbhelper.getcursor()
        query = "DELETE FROM  author WHERE author_name = '%s'"%(username)
        ##print query
        cur.execute(query)
        dbhelper.commit()
    def addauthor(self,dbhelper,username,pwd,nick_name,server_id=1):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        import utility
        user_id =utility.getid()
        query = "INSERT INTO author VALUES('%s','%s','%s',%s,'%s')"%(user_id,username,pwd,server_id,nick_name)
        ##print query
        cur.execute(query)
        dbhelper.commit()
        return user_id
if __name__ == '__main__':
    dbhelper = Databasehelper()
    authorhelper = AuthorHelper()
    import utility
    username = utility.getid()
    authorhelper.addauthor(dbhelper,username,"12345","Test-"+username)
    print authorhelper.authorauthenticate(dbhelper,username,"12345")
    authorhelper.deleteauthor(dbhelper,username)
