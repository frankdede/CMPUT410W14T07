import json
class Message:
    """
    to store message information
    """
    def __init__(self,recipient,sender,time,read=0):
        self.recipient = recipient
        self.sender = sender
        self.time = time
        self.status = status
    def __str__(self):
        return self.tojson()
    def tojson(self):
        return {"recipient":self.recipient,"sender":self.sender,"time":self.time,"status":self.status}
    def __eq__(self,other):
        return (self.request_name == other.request_name and self.requested_name == other.requested_name and self.time == other.time and self.read == other.read)
    def jsonToMessage(jsonstring):
        dic = json.loads(jsonstring)
        return Message(dic["request_name"],dic["requested_name"],dic["time"],dic["read"])