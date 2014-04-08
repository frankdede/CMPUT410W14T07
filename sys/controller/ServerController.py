import json
from mysql.connector.errors import Error
from DatabaseAdapter import *
from ServerHelper import *
class ServerController:

    def __init__(self,dbAdapter):
        self.serverHelper = ServerHelper(dbAdapter)
    
    '''check whether the server exists or not'''
    def doesServerExists(self,url):

        result = self.serverHelper.doesServerExists(url)
        return result
        
    ''' add new server'''
    def addServer(self,name,url,local):
    
        return self.serverHelper.addServer(name,url,local)
