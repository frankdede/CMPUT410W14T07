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
        query = "SELECT * FROM author WHERE author_name=%s AND sid=1"
        cur.execute(query,(username))
        if cur.fetchone() is None:
            return False
        else:
            return True
    # to add an author to database the server_id is defualtly 1 if server_id is not provided
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
if __name__ == '__main__':
    dbhelper = Databasehelper()
    authorhelper = AuthorHelper()
    authorhelper.addauthor(dbhelper,"Admin","12345","Administrator")
    print authorhelper.authorauthenticate(dbhelper,"Admin","12345")
