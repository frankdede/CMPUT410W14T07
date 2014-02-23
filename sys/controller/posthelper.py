from databasehelper import *
from model/post import *
from databasehelper import *
class PostHelper:
    """
    to check the author whether is existed
    """
    def insertpost(self,dbhelper,post):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        pid = post.getpid()
        aid = post.getaid()
        title = post.gettitle()
        message = post.getmessage()
        type = post.gettype()
        permission = post.getpermission()
        query = "INSERT INTO post VALUES('%s','%s',SYSDATE(),'%s','%s','%s','%s')"%(pid,aid,title,message,type,permission)
        cur.execute(query)
        dbhelper.commit()
#type argument should be one of ['pid','aid','title','message','title','permission']
#Ussage: updatepost(type="html", permmision="public") check keyword argument
    def updatepost(self,dbhelper,**kargs):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        for type in kargs:
            if type in ['pid','aid','dates','message','title','permission']:
                if type == 'type' and newcontent in['html','txt','markdown']:
                    pass
                elif type == 'permission' and newcontent in['me','user','friends','fof','fomh','public']:
                    pass
                else:
                    query = "UPDATE post SET %s='%s'"%(type,kargs[type])
                    print query
                    cur.execute(query)
                    dbhelper.commit()
# delete a post or server post by pid, aid,you need indicate in type argument
    def deletepost(self,dbhelper,type,key):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        if type == "pid":
            query = "DELETE FROM post WHERE pid = '%s'"%(key)
        elif type == "aid":
            query = "DELETE FROM post WHERE aid = '%s'"%(key)
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
