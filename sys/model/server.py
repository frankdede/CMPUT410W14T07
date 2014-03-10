##server model
class Server:
    def __init__(self,sid,serve_name,url):
        self.sid = sid
        self.server_name = server_name
        self.url = url
    def setsid(self,sid):
        self.sid = sid
    def setservername(self,server_name):
        self.server_name =server_name
    def setserverurl(self,url):
        self.url = url
    def getsid(self):
        return self.sid
    def getservername(self):
        return self.server_name
    def geturl(self):
        return self.url
