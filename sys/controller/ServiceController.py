import mysql.connector
from CircleController import *
from RequestController import *
import json

class ServiceController:

    def __init__(self, dbAdapter):
        self.circleController = CircleController(dbAdapter)
        self.requestController = RequestController(dbAdapter)
    def registerRemoteServer():
        pass

    def authenticRemoteServer():
        pass

    '''
    Determine if two authors are friends or not

    Status of the repsone will be 'YES' if two authors are friends
    else 'NO' 
    '''
    def checkFriendsForRemoteServer(aid1,aid2):
        
        result = self.circleController.areFriends(aid1,aid2)
        if(result != None):
            response = {}
            response['query'] = 'friends'
            if(result):
                response['friends'] = 'YES'
            else:
                response['friends'] = 'NO'
            return json.dumps(response)

        return None

    '''
    Check if the authors in the list are friends of a specific author for remote server
    '''
    def checkAuthorsListForRemoteServer(request):

        if(request['query'] == 'friends'):
            author = request['author']
            authorsList = request['authors']

            result = self.circleController.areFriendsOfAuthor(author,authorsList)

            response = {}
            response['query'] = 'friends'
            response['author'] = author
            response['friends'] = result
            return json.dumps(repsonse)
        return None

    def receiveFriendRequestFromRemoteServer(request):

        if(request['query'] == 'friendrequest'):
            localAid = request['id']
            remoteServer = request['friend']['author']['host']
            remoteDisplayName  = request['friend']['author']['displayname']
            remoteAid = request['friend']['author']['id']
            
            result = self.requestController.sendRequest(remoteAid,localAid)

            if result == True :
                return True
            else:
                return False
        return None

    def sendFriendRequestToRemoteServer(senderAid,senderName,remoteAid,remoteSid):

        request = {}
        response['query'] = 'friendrequest'
        friend = {}

        friend['id'] = remoteAid
        friend['host'] = remoteSid
        friend['displayname'] = name

        author = {}
        author['id'] = senderAid
        author['host'] = "http://cs410.cs.ualberta.ca:41070/"
        author['displayname'] = senderName
        request['friend'] = friend

        return jason.dumps(request)






        

