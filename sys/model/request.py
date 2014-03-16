import json
class Request:
    """
    Request object(sid,sender's name, time)
    """
    def __init__(self,sid,sender,time):
        self.sid = sid
        # this is not sender_id
        self.sender = sender
        self.time = time
    def tojosn(self):
        return {"sid":self.sid,"sender":self.sender,"time":self.time}

def parse(jsonstring):
    dic = json.loads(jsonstring)
    return Request(dic["sid"],dic["sender"],dic["time"])

def parseList(jsonstring):
    result = []
    dic = json.loads(jsonstring)
