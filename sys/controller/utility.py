import uuid
def getid():
    return str(uuid.uuid4())
def gettime():
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S')
