import json

class Author:
    def __init__(self,aid,name,email,city,imgPath,sid,nickName):

        self.aid = aid
        self.name = name
        self.sid = sid
        self.email = email
        self.ciyt = city
        self.imgPath = imgPath
        self.nickName = nickName

    def setAuthorName(self,aname):
        self.name = name

    def setPassword(self,password):
        self.pwd = password

    def setAid(self,aid):
        self.aid = aid

    def setSid(self,sid):
        self.sid = sid

    def setNickname(self,nickName):
        self.nickName = nickName

    def setImagePath(self,imgPath):
        self.imgPath = imgPath

    def setCity(self,city):
        self.city = city

    def getAuthorName(self):
        return self.name

    def getAid(self):
        return self.aid

    def getPassword(self):
        return self.pwd

    def getSid(self):
        return self.sid

    def getNickname(self):
        return self.nickName

    def tojson(self):
        return {"aid":self.aid,"name":self.name,"email":self.email,"city":self.city,"nick_name":self.nick_name,"sid":self.sid,"img_path":self.imgPath}

    def jsontoauthor(jsonstring):
        
        dic = json.loads(jsonstring)
        return Author(dic["aid"],dic["aname"],dic["sid"],dic["nickname"])
