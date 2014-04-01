import json

class Author:
    def __init__(self,aid,name,nickName,sid,email,gender,city,birthday,imgPath):

        self.aid = aid
        self.name = name
        self.sid = sid
        self.gender = gender
        self.email = email
        self.city = city
        self.imgPath = imgPath
        self.nickName = nickName
        self.birthday = birthday

    def setName(self,aname):
        self.name = name

    def setAid(self,aid):
        self.aid = aid

    def setGender(self,gender):
        self.gender = gender

    def setSid(self,sid):
        self.sid = sid

    def setNickname(self,nickName):
        self.nickName = nickName

    def setImagePath(self,imgPath):
        self.imgPath = imgPath

    def setCity(self,city):
        self.city = city

    def setBirthday(self,birthday):
        self.birthday = birthday

    def getName(self):
        return self.name

    def getAid(self):
        return self.aid

    def getGender(self):
        return self.gender

    def getSid(self):
        return self.sid

    def getNickname(self):
        return self.nickName

    def getBirthday(self):
        return self.birthday

    def tojson(self):
        result = {}
        result['id'] = self.aid
        result['host'] = self.sid
        result['displayname'] = self.nick_name
        result['username'] = self.name
        result['email'] = self.email
        result['gender'] = self.gender
        result['city'] = self.city
        result['birthday'] = self.birthday
        result['imgPath'] = self.imgPath
        result['url'] = None
        
        return result
