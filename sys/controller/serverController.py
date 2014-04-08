import json
from mysql.connector.errors import Error
from DatabaseAdapter import *

class ServerController:

    def __init__(self,dbAdapter):
        self.serverController = ServerController(dbAdapter)
    
    def doesServerExists(self,url):
    '''check whether the server exists or not'''

        return self.serverHelper.doesServerExists(url)

    def addServer(self,name,url,local):
    ''' add new server'''

        return self.serverHelper.addServer(name,url,local)
