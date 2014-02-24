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
# for the specific person permission, you need to add it to user_permission table
    def addpostpermission(self,dbhelper,pid,aid):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query = "INSERT INTO user_permission VALUES('%s','%s')"%(pid,aid)
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
# get list of post that the user by aid can browse
    def getpostlist(self,dbhelper,aid):
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        #get permission with public
        query = "SELECT * FROM post WHERE permission='public'"
        cur.execute(query)
        re = []
        for fid in cur:
            re.append(fid)
        utility.addpath('../model')
        #get permission with me
        query = "SELECT * FROM post WHERE permission='me' and aid='%s'"%(aid)
        cur.execute(query)
        for fid in cur:
            re.append(fid)
        #get permission with user
        query = "SELECT * FROM post WHERE permission = 'user' and pid IN (SELECT pid from user_permission WHERE aid='%s')"%(aid)
        cur.execute(query)
        for fid in cur:
            re.append(fid)
        #get permission with friends
        import authorhelper
        author_name = AuthorHelper().getnamebyaid(dbhelper,aid)
        query = "SELECT * FROM post WHERE permission = 'friends' and aid IN  (SELECT aid from author WHERE author_name IN (SELECT name1 FROM circle WHERE name2 ='%s' ))"%(author_name)
        cur.execute(query)
        for fid in cur:
            re.append(fid)
        #get permission with fof
        query = "SELECT * FROM post WHERE permission = 'fof' and aid IN  (SELECT aid from author WHERE author_name IN (SELECT name1 FROM circle WHERE name2 IN (SELECT name1 FROM circle WHERE name2 = '%s')))"%(author_name)
        cur.execute(query)
        print query
        for fid in cur:
            re.append(fid)
        #get permission with friends
        
        return re
if __name__ == '__main__':
    dbhelper = Databasehelper()
    posthelper = PostHelper()
    import utility
    pid = utility.getid()
    time = utility.gettime()
    utility.addpath('../model')
    from  authorhelper import *
    aid = AuthorHelper().getaidbyname(dbhelper,"test3")
    from  post import *
    li = posthelper.getpostlist(dbhelper,aid)
    for i in li:
        print i