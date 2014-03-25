import json
class Comment:
    def __init__(self,cid,aid,nickName,time,content):
        self.cid = cid
        self.aid = aid
        self.nickName = nickName
        self.time = time
        self.content = content

    def getCid(self):
        return self.cid

    def getAid(self):
        return self.aid

    def getTime(self):
        return self.time

    def getNickName(self,nickName):
        return self.nickName

    def getContent(self):
        return self.content

    def setCid(self,cid):
        self.cid = cid

    def setAid(self,aid):
        self.aid = aid

    def setTime(self,time):
        self.time = time

    def setNickName(self,nickName):
        self.nickName = nickName

    def setContent(self,content):
        self.content = content

    def tojson(self):
        result = {}
        result['cid'] = self.cid
        result['aid'] = self.aid
        result['nick_name'] = self.nickName
        result['content'] = self.content
        result['time'] = self.time
        return result

def parse(jsonstring):
    dic = json.loads(jsonstring)
    post = Post()
    post.setCid(dic['cid'])
    post.setAid(dic['aid'])
    post.setDate(dic['time'])
    post.setContent(dic['content'])
    post.setName(dic['nick_name'])
    return post




