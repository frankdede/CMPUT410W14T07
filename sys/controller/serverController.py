import json
from mysql.connector.errors import Error
from DatabaseAdapter import *

class ServerController:

    def __init__(self,dbAdapter):
        self.serverController = ServerController(dbAdapter)

    def doesServerExists(self,url):
        return self.serverHelper.doesServerExists(url)

    def addServer(self,name,url,local):
        return self.serverHelper.addServer(name,url,local)