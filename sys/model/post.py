class Post:
    def __init__(self,aid,dates,title,message,type,permission):
        self.aid = aid
        self.dates = dates
        self.title=title
        self.message=message
        self.type=type
        self.permission=permission
    def getdates(self):
        return self.dates
    def getaid(self):
        return self.aid
    def gettitle(self):
        return self.title
    def getmessage(self):
        return self.message
    def gettype(self):
        return self.type
    def getpermission(self):
        return self.permission
    def setaid(self,aid):
        self.aid = aid
    def settitle(self,title):
        self.title = title
    def setmessage(self,message):
        self.message=message
    def setpermission(self,permission):
        self.permission=permission
    def setdates(self,dates):
        self.dates = dates
    def tojson(self):
        import json
        return json.dumps({"aid":self.aid,"date":self.dates,"title":self.title,"message":self.message,"type":self.type,"permit":self.permission})
    def jsontopost(self,jsonstring):
        import json
        dic = json.loads(jasonstring)
        return Post(dic[aid],dic[date],dic[title],dic[message],dic[type],dic[permission])
    def __eq__(self,other):
if __name__=='__main__':
    a = Post(123,"dsada",2332,"adsasd",1212,"dsadas")
    print a.tojson()
