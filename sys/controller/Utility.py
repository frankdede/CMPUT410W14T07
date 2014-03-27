import uuid
import re
def getid():
    return str(uuid.uuid4())
def gettime():
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S')
def addpath(path):
    import sys
    sys.path.insert(0,path)
def parseKeyword(raw_input):
    if raw_input == None or raw_input =="":
        return None
    return raw_input.split(" ")
#return re.findall(r'\W+',raw_input)
    