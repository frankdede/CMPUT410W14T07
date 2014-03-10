import json
class Post:
    def __init__(self,pid,aid,dates,title,message,type,permission):
        self.pid = pid
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
    def getpid(self):
        return self.pid
    def tojson(self):
        return {"pid":self.pid,"aid":self.aid,"date":self.dates,"title":self.title,"message":self.message,"type":self.type,"permit":self.permission}
    def __eq__(self,other):
        return (self.aid==other.aid and self.dates==other.dates and self.title==other.title and self.message==other.message and self.type==other.type and self.permission==other.permission)
#convert from object to json file
    def jsontopost(jsonstring):
        dic = json.loads(jsonstring)
        return Post(dic["pid"],dic["aid"],dic["date"],dic["title"],dic["message"],dic["type"],dic["permit"])