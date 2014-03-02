from databasehelper import *
class PostHelper:
    """
    an post helper,which controls the post model
    """
    def insertpost(self,dbhelper,post):
        """
        to add a post to databse
        dbhelper -- the databasehelper
        post -- the post object
        """
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
        return cur.rowcount>0
    def addpostpermission(self,dbhelper,pid,aid):
        """add a user permission to post in databse
        dbhelper -- databse helper
        pid -- post id
        aid -- author id
        """
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query = "INSERT INTO user_permission VALUES('%s','%s')"%(pid,aid)
        print query
        cur.execute(query)
        dbhelper.commit()
        return cur.rowcount>0
#type argument should be one of ['pid','aid','time','message','title','permission']
#Ussage: updatepost(databasehelper,pid,type="html", permmision="public") check keyword argument
    def updateMessage(self,dbhelper,pid,newcontent):
        """ 
            to update the message in post
            Keyword arguments:
            dbhelper  -- database helper
            pid -- post id
            newcontent -- the new Content in post
            """
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query = "UPDATE post SET message='%s' WHERE pid='%s'"%(newcontent,pid)
        cur.execute(query)
        dbhelper.comit()
        return cur.rowcount>0
    def updateTitle(self,dbhelper,pid,newtitle):
        """
        to update the title of post
        pid -- post id
        newtitle -- new title need to be updated
        """
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query = "UPDATE post SET title='%s' WHERE pid='%s'"%(newtitle,pid)
        cur.execute(query)
        dbhelper.comit()
        return cur.rowcount>0
    def updateTime(self,dbhelper,pid,time = ''):
        """
        to update the time of post
        time -- time format should be like 2014-03-01 01:37:50, the default time is current time.
        """
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        if time  == '':
            query = "UPDATE post SET time=NULL WHERE pid='%s'"%(pid)
        else:
            query = "UPDATE post SET time='%s' WHERE pid='%s'"%(time,pid)
        cur.execute(query)
        dbhelper.comit()
        return cur.rowcount>0
# if you need change to permission to user, you need to specify the user aid    
    def updatePermission(self,dbhelper,pid,newpermission,user=''):
        """
        to update the permission
        pid -- post id
        newpermission -- the new permission need to be update
        user -- if the new permission is user, user is the aid
        """
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query = "UPDATE post SET permission='%s' WHERE pid='%s'"%(newpermission,pid)
        cur.execute(query)
        if newpermission == 'user':
            self.adduserpermission(dbhelper,pid,user)
        else:
            query = "DELETE FROM user_permission WHERE pid='%s'"%(pid)
        cur.execute(query)
        dbhelper.commit()
    def deletepostbyid(self,dbhelper,pid):
        """
         delete a post or server post by pid, aid
        dbhelper -- database helper
        pid -- post id
        """
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query=""
        if type == "pid":
            query = "DELETE FROM post WHERE pid = '%s'"%(key)
        cur.execute(query)
        dbhelper.commit()
        return cur.rowcount>0
    def deletepostbyaid(self,dbhelper,aid):
        """
        to delete a post by authorid
        aid -- author id
        dbhelper -- database helper
        """
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        query=""
        if type == "aid":
            query = "DELETE FROM post WHERE aid = '%s'"%(aid)
        cur.execute(query)
        dbhelper.commit()
        return cur.rowcount>0
    def getpostlist(self,dbhelper,aid):
        """
        get list of post that the user by aid can browse
        aid -- author id
        """
        if not isinstance(dbhelper,Databasehelper):
            raise NameError('invalid argument')
        if not dbhelper.isconnect():
            dbhelper.connect()
        cur = dbhelper.getcursor()
        #get the post if it is public
        query = "SELECT * FROM post WHERE permission='public'"
        cur.execute(query)
        re = []
        for fid in cur:
            re.append(fid)
        utility.addpath('../model')
        #get the post if aid is its author
        query = "SELECT * FROM post WHERE permission='me' and aid='%s'"%(aid)
        cur.execute(query)
        for fid in cur:
            re.append(fid)
        #get the post if aid is specifiied user
        query = "SELECT * FROM post WHERE permission = 'user' and pid IN (SELECT pid from user_permission WHERE aid='%s')"%(aid)
        cur.execute(query)
        for fid in cur:
            re.append(fid)
        #get the post if aid is the author's friend
        import authorhelper
        author_name = AuthorHelper().getnamebyaid(dbhelper,aid)
        query = "SELECT * FROM post WHERE permission = 'friends' and aid IN  (SELECT aid from author WHERE author_name IN (SELECT name1 FROM circle WHERE name2 ='%s' ))"%(author_name)
        cur.execute(query)
        for fid in cur:
            re.append(fid)
        #get the post if aid is the author's friends`s friend
        query = "SELECT * FROM post WHERE permission = 'fof' and aid IN  (SELECT aid from author WHERE author_name IN (SELECT name1 FROM circle WHERE name2 IN (SELECT name1 FROM circle WHERE name2 = '%s')))"%(author_name)
        cur.execute(query)
        print query
        for fid in cur:
            re.append(fid)
        #get the post if aid is in the same host as the permission's requirement
        query = "SELECT * FROM post WHERE permission='fomh' AND aid IN (SELECT a1.aid FROM author a1,author a2 WHERE a1.sid = a2.sid AND a2.aid = '%s')"%(aid)
        print query
        cur.execute(query)
        for fid in cur:
            re.append(fid)
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
