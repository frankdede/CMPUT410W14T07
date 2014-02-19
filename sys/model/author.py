class author:
    def __init__(self,aid,pwd,sid,nick_name):
        self.aid=aid
        self.pwd=pwd
        self.sid=sid
        self.nick_name=nick_name
    def setpassword(self,password):
        self.pwd=password
    def setauthorid(self,aid):
        self.aid=aid
    def setsid(self,sid):
        self.sid=sid
    def setnickname(self,nick_name):
        self.nick_name=nick_name
    def getaid(self):
        return self.aid
    def getpwd(self):
        return self.pwd
    def getsid(self):
        return self.sid
    def getnickname(self):
        return self.nick_name
import json
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, author):
            return [obj.aid, obj.pwd]
        return json.JSONEncoder.default(self, obj)
if __name__ =="__main__":
    import json
    a = author(132,123,123,123)
    b = json.dumps(a,cls=ComplexEncoder)
    print b
