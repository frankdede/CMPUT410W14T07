import json
import server
import author
import circle
import post
class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, server):
            return [obj.sid, obj.]
    return json.JSONEncoder.default(self, obj)
if __name__ =="__main__":
   a =  author.Author("a",121,121,1212)
