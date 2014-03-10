import json
class circle:
    def __init__(self,author1,author2):
        self.author1=author1
        self.author2=author2
    def __str__(self):
        return self.author1+ " "+self+author2
    def __eq__(self,other):
        return self.author1 == other.author1 and self.author2==other.author2
    def tojson(self):
        return {"author1":self.author1,"author2":self.author2}
    def jsontocircle(jsonstring):
        import json
        dic = json.loads(jsonstring)
        return circle(dic["author1"],dic["author2"])