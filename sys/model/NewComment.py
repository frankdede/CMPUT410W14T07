import NewAuthor
import json
class NewComment:
    def __init__(self,author,content,date,cid):
        self.cid = cid
        self.author = author
        self.content = content
        self.time = time
    '''
    Getters
    '''
    def getCid(self):
        return self.cid

    def getAuthor(self):
        return self.author

    def getTime(self):
        return self.time

    def getContent(self):
        return self.content

    '''
    Setters
    '''
    def setCid(self,cid):
        self.cid = cid

    def setAuthor(self,author):
        self.author = author

    def setTime(self,time):
        self.time = time

    def setContent(self,content):
        self.content = content

    def tojson(self):
        result = {}
        result['guid'] = self.cid
        result['author'] = self.author.tojson()
        result['comment'] = self.content
        result['pubDate'] = self.time
        return result