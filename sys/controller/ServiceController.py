import mysql.connector
from CircleController import *
from RequestController import *
from PostController import *
from CommentController import *
from AuthorController import *
from ServerController import *
import json

class ServiceController:

    def __init__(self, dbAdapter):
        self.circleController = CircleController(dbAdapter)
        self.requestController = RequestController(dbAdapter)
        self.commentController = CommentController(dbAdapter)
        self.authorController = AuthorController(dbAdapter)
        self.serverController = ServerController(dbAdapter)
        self.postController = PostController(dbAdapter)
    def registerRemoteServer():
        pass

    def authenticRemoteServer():
        pass

    '''
    Determine if two authors are friends or not

    Status of the repsone will be 'YES' if two authors are friends
    else 'NO' 
    '''
    def checkFriendsForRemoteServer(self,aid1,aid2):
        
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
    def checkAuthorsListForRemoteServer(self,request):

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

    def receiveFriendRequestFromRemoteServer(self,request):
        '''receive friend request from remote server'''

        if(request['query'] == 'friendrequest'):
            localAid = request['friend']['author']['id']
            localServer = request['friend']['author']['host']

            remoteServer = request['author']['host']
            remoteDisplayName  = request['author']['displayname']
            remoteAid = request['author']['id']
            
            
            serverId = self.serverController.doesServerExists(remoteServer)

            if(serverId == False):
                serverId = self.serverController.addServer(remoteServer,remoteServer,0)

            print(remoteAid)
            result = self.authorController.doesAuthorExists(remoteAid)
            print(result)

            if(result != True):
                self.authorController.addRemoteAuthor(remoteAid,remoteAid,serverId)

            result = self.requestController.sendRequest(remoteAid,localAid)

            if(result == True):
                return True
            else:
                return False
        return None

    def sendFriendRequestToRemoteServer(self,senderAid,senderName,remoteAid,remoteUrl):
        '''send friend request to remote server'''

        request = {}
        request['query'] = 'friendrequest'
        friend = {}

        friend['id'] = remoteAid
        friend['host'] = remoteUrl
        friend['displayname'] = ''

        request['id'] = senderAid
        request['host'] = "http://cs410.cs.ualberta.ca:41078/"
        request['displayname'] = senderName
        request['friend'] = friend

        return request

    def sendPublicPostsToRemoteServer(self):
        '''send the public posts to remote server'''
        jsonObj = {}
        posts = self.postController.getLocalPublicPosts()
        comments = self.commentController.getCommentsForPublicPosts()
        if(posts != None and comments != None):
            for post in posts:
                for comment in comments:
                    if(post['guid'] == comment['pid']):
                        post['comments'].append(comment)
            jsonObj['posts'] = posts 
            return jsonObj

        else:
            return {}

    def sendGlobalAuthorsToRemoteServer(self):
        '''send global authors to remote server'''

        authors = self.authorController.getGlobalAuthors()

        if authors != None:
            return authors
        else:
            return []

    def getGlobalAuthorsFromRemoteServer(self):

        #self.postController.addPosts
        pass

    def getPublicPostsFromRemoteServer(self):

        pass
 



                


        

