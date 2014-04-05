import mysql.connector
from CircleController import *
from RequestController import *
import json

class ServiceController:

    def __init__(self, dbAdapter):
        self.circleController = CircleController(dbAdapter)
        self.requestController = requestController(dbAdapter)
    '''
    A response if friends or not
    '''
    def checkFriendsForRemoteServer(aid1,aid2):
        
        result = self.circleController.areFriends(aid1,aid2)
        if(result != None):
            response = {}
            response['query'] = 'friends'
            response['friends'] = [aid1,aid2]
            if(result):
                response['status'] = 'YES'
            else:
                response['status'] = 'NO'
            return response

        return None
    '''
    '''
    def checkAuthorsListForRemoteServer(request):
        if(request['query'] == 'friends'):
            author = request['author']
            authorsList = request['authors']

            result = self.circleController.isFriendOfAuthor(author,authorsList)

            response = {}
            response['query'] = 'friends'
            response['author'] = author
            response['friends'] = result
            return repsonse

        return None


