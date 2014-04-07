import json
class Image:
    """
        To keep the image information
        """
    def __init__(self,iid,path,time,aid,pid):
        self.iid = iid
        self.path = path
        self.time = time
        self.aid = aid
        self.pid = pid
    def getPath(self):
        return self.path
    def getIid(self):
        return self.iid
    def getTime(self):
        return self.time
    def getAid(self):
        return self.aid
    def getPid(self):
        return self.pid
    def setIid(self,iid):
        self.iid = iid
    def setPath(self,path):
        self.path = path
    def setTime(self,time):
        self.time = time
    def setAid(self,aid):
        self.aid = aid
    def setPid(self,pid):
        self.pid = pid
    def toJson(self):
        return {"iid":self.aid,"time":self.time,"aid":self.aid,"pid":self.pid}