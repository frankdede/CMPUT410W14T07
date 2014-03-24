import json
class Comment:
    def __init__(self,cid,name,aid,date,content):
        self.cid = cid
        self.aid = aid
        self.name = name
        self.date = date
        self.content = content

    def getCid(self):
        return self.cid

    def getAid(self):
        return self.aid

    def getDate(self):
        return self.date

    def getContent(self):
        return self.content

    def setCid(self,cid):
        self.cid = cid

    def setAid(self,aid):
        self.aid = aid

    def setDate(self,date):
        self.date = date

    def setContent(self,content):
        self.content = content


