class Message:
    """
    to store message information
    """
    def __init__(self,request_name,requested_name,time,read="0"):
        self.request_name = request_name
        self.requested_name = requested_name
        self.time = time
        self.read = read
    def __str__(self):
        return self.tojson()
    def tojson(self):
        import json
        return json.dumps({"request_name":self.request_name,"requested_name":self.requested_name,"time":self.time,"read":self.read})
    def __eq__(self,other):
        return (self.request_name == other.request_name and self.requested_name == other.requested_name and self.time == other.time and self.read == other.read)
def jsonToMessage(jsonstring):
    import json
    dic = json.loads(jsonstring)
    return Message(dic["request_name"],dic["requested_name"],dic["time"],dic["read"])
if __name__ == '__main__':
    a = Message("12345","54321","2014-03-21","1")
    print a == jsonToMessage(a.tojson())
    print a
