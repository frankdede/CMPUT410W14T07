class Author:
    def __init__(self,aid,aname,pwd,sid,nick_name=''):
        self.aid=aid
        self.aname = aname
        self.pwd=pwd
        self.sid=sid
        self.nick_name=nick_name
    def setauthorname(self,aname):
        self.aname= aname
    def setpassword(self,password):
        self.pwd=password
    def setauthorid(self,aid):
        self.aid=aid
    def setsid(self,sid):
        self.sid=sid
    def setnickname(self,nick_name):
        self.nick_name=nick_name
    def getauthorname(self):
        return self.aname
    def getaid(self):
        return self.aid
    def getpwd(self):
        return self.pwd
    def getsid(self):
        return self.sid
    def getnickname(self):
        return self.nick_name
    def __eq__(self,other):
        return self.aid == other.aid and self.aname == self.aname and self.pwd == other.pwd and self.sid == other.sid
    def tojson(self):
        import json
        return json.dumps({"aid":self.aid,"aname":self.aname,"pwd":self.pwd,"nickname":self.nick_name,"sid":self.sid})
def jsontoauthor(jsonstring):
    import json
    dic = json.loads(jsonstring)
    return Author(dic["aid"],dic["aname"],dic["pwd"],dic["sid"],dic["nickname"])
if __name__ =="__main__":
    import json
    a = Author("132","123","123","123","sada")
    b = a.tojson()
    print a == jsontoauthor(b)
