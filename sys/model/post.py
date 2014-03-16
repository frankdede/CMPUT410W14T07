import json
class Post:
    def __init__(self,pid,aid,date,title,content,type,permission):
        self.pid = pid
        self.aid = aid
        self.date = date
        self.title=title
        self.content=content
        self.type=type
        self.permission=permission

    def getDate(self):
        return self.date

    def getAid(self):
        return self.aid

    def getTitle(self):
        return self.title

    def getContent(self):
        return self.content

    def getType(self):
        return self.type

    def getPermission(self):
        return self.permission

    def setAid(self,aid):
        self.aid = aid

    def setTitle(self,title):
        self.title = title

    def setContent(self,message):
        self.content = content

    def setPermission(self,permission):
        self.permission = permission

    def setDate(self,dates):
        self.date = date

    def getPid(self):
        return self.pid

    def tojson(self):
        return {"pid":self.pid,"aid":self.aid,"date":self.date,"title":self.title,"content":self.content,"type":self.type,"permission":self.permission}

#convert from object to json file
def parse(jsonstring):
    dic = json.loads(jsonstring)
    return Post(dic["pid"],dic["aid"],dic["date"],dic["title"],dic["content"],dic["type"],dic["permission"])

def parseList(jsonstring):
    result = []
    dic = json.loads(jsonstring)
    for post in dic:
        result.append(Post(dic["pid"],dic["aid"],dic["date"],dic["title"],dic["content"],dic["type"],dic["permission"]))
    return result
