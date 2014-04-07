from CircleHelper import *
import json

class CircleController:

    circleHelper = None

    def __init__(self,dbAdapter):
        self.circleHelper = CircleHelper(dbAdapter)
    
    '''
    Add friend for an authorf13 x
    NOTE:Two-way Insertion
    @param String aid1
    @param String aid2
    @return Boolean Returns True if adding successfully,else False
    '''
    def addFriendForAuthor(self,aid1,aid2):

        return self.circleHelper.addFriendForAuthor(aid1,aid2)

    '''
    Delete Author's Friend by aid and his/her friend's aid
    NOTE:Two-way deletion
    @param String aid1
    @param String aid2
    @return Boolean Returns True if adding successfully,else False
    '''
    def deleteFriendOfAuthor(self,aid1,aid2):

        return self.circleHelper.deleteFriendOfAuthor(aid1,aid2)

    def getFriendList(self,aid):
    '''get friend list by author id'''

        result = self.circleHelper.getFriendList(aid)

        if(result != None):

            friendList = []
            for row in result:
                friend = Author(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                friendList.append(friend.tojson())
            return json.dumps(friendList)

        return None

    def getFriendOfMyHomeServerList(self,aid):
    '''get a list of all friend by author id on local server'''

        result = self.circleHelper.getFriendOfMyHomeServerList(aid)

        if(result != None):

            friendList = []
            for row in result:
                friend = Author(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                friendList.append(friend.tojson())
            return json.dumps(friendList)

        return None

    def getFriendOfFriendList(self,aid):
        '''get a list of all friend of friends by author id'''
        result = self.circleHelper.getFriendOfFriendList()

        if(result != None):
            friendList = []
            for row in result:
                friend = Author(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                friendList.append(friend.tojson())
            return json.dumps(friendList)

        return None 

    def areFriends(self,aid1,aid2):
        '''check whether two users are friends or not'''
        return self.circleHelper.areFriends(aid1,aid2)

    def areFriendsOfAuthor(self,author,authorsList):
       '''check all author's friends'''

        rows = self.circleHelper.areFriendsOfAuthor(author,authorsList)

        if(rows != None):
            friendsList = []
            for row in rows:
                friendsList.append(row[0])

            return friendsList
        else:
            return None

