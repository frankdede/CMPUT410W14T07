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

    def setPassword(self,password):
        self.pwd = password

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

    def setbirthday(self, birthday):
        self.birthday = birthday

    def getName(self):
        return self.name

    def getAid(self):
        return self.aid

    def getPassword(self):
        return self.pwd

    def getGender(self):
        return self.gender

    def getSid(self):
        return self.sid

    def getNickname(self):
        return self.nickName

    def getbirthday(self, birthday):
        return self.birthday

    def tojson(self):
        return {"aid":self.aid,"name":self.name,"nick_name":self.nickName,"sid":self.sid,"email":self.email,"gender":self.gender,"city":self.city,"birthday":self.birthday,"img_path":self.imgPath}

def parse(jsonstring):
        
    dic = json.loads(jsonstring)
    return Author(dic["aid"],dic["name"],dic["nick_name"],dic["sid"],dic["email"],dic["gender"],dic['city'],dic['birthday'],dic['img_path'])
def parseList(jsonstring):
    result = []
    dic = json.loads(jsonstring)
    for author in dic:
        result.append(Author(dic["aid"],dic["name"],dic["nick_name"],dic["sid"],dic["email"],dic["gender"],dic['city'],dic['birthday'],dic['img_path']))
    return result

