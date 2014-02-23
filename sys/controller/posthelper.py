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
        query = "INSERT INTO post VALUES('%s','%s',NULL,'%s','%s','%s','%s')"%(pid,aid,title,message,type,permission)
        print query
        cur.execute(query)
        dbhelper.commit()
#type argument should be one of ['pid','aid','time','message','title','permission']
#Ussage: updatepost(type="html", permmision="public") check keyword argument
    def updatepost(self,dbhelper,**kargs):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        for type in kargs:
            if type in ['pid','aid','time','message','title','permission']:
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
        query=""
        if type == "pid":
            query = "DELETE FROM post WHERE pid = '%s'"%(key)
        elif type == "aid":
            query = "DELETE FROM post WHERE aid = '%s'"%(key)
        print query
        cur.execute(query)
        dbhelper.commit()
if __name__ == '__main__':
    dbhelper = Databasehelper()
    posthelper = PostHelper()
    import utility
    pid = utility.getid()
    time = utility.gettime()
    utility.addpath('../model')
    from  authorhelper import *
    aid = AuthorHelper().getaidbyname(dbhelper,"test1")
    from  post import *
    posthelper.insertpost(dbhelper,Post(pid,aid,time,"helloworld","Test content","txt","public"))
