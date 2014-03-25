import json
class Post:
    def __init__(self,pid,aid,name,date,title,content,commentList,type,permission):
        self.pid = pid
        self.aid = aid
        self.name = name
        self.date = date
        self.title=title
        self.content=content
        self.type=type
        self.permission=permission
        self.commentList = commentList

    def getPid(self):
        return self.pid

    def getDate(self):
        return self.date

    def getAid(self):
        return self.aid

    def getName(self):
        return self.name

    def getTitle(self):
        return self.title

    def getContent(self):
        return self.content

    def getType(self):
        return self.type

    def getComments(self):
        return self.comments

    def getPermission(self):
        return self.permission

    def setAid(self,aid):
        self.aid = aid

    def setName(self,name):
        self.name = name

    def setTitle(self,title):
        self.title = title

    def setContent(self,message):
        self.content = content

    def setPermission(self,permission):
        self.permission = permission

    def setDate(self,dates):
        self.date = date

    '''
        Convert Post object to a dictionary
        @return Dictionary Returns a dictionary of 
    '''
    def tojson(self):
        result = {}
        commentsDict = {}
        result['pid'] = self.pid
        result['aid'] = self.aid
        result['name'] = self.name
        result['tilte'] = self.title
        result['date'] = self.date
        result['content'] = self.content
        result['type'] = self.type
        result['permission'] = self.permission

        if(self.commentList != None):
            for comment in self.commentList:
                commentsDict[comment.getCid()] = comment.tojson()
        result['commentList'] = commentsDict

        return result

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
