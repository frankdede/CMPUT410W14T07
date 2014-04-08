import mysql.connector
from CircleController import *
from RequestHelper import *
import json

class RequestController:

  def __init__(self,dbAdapter):
    self.requestHelper = RequestHelper(dbAdapter)
    self.circleController = CircleController(dbAdapter)
  '''
    accept the request from sender
  '''
  def acceptRequestFromSender(self,recipientId,senderId):

    result = self.circleController.addFriendForAuthor(recipientId,senderId)
    if (result == True):
      return self.requestHelper.deleteRequest(recipientId,senderId)
    return False

  '''
    (The Order of passing parameters matters)
    @param String senderId
    @param String recipientId
    @return Boolean 
  '''
  def sendRequest(self,senderId,recipientId):

    return  self.requestHelper.addNewRequest(recipientId,senderId)

  '''
    Delete a request by recipient ID and sender ID
    (The Order of passing parameters matters)
    @param String recipientId
    @param String senderId
    @return Boolean 
  '''
  def deleteRequest(self,recipientId,senderId):

    return  self.requestHelper.deleteRequest(recipientId,senderId)

  '''
    Get all the requests content based on recipient ID
    @param String recipientId
    @return String JSON String 
  '''
  def getAllRequestByAid(self,recipientId):

    requestList = []
    result = self.requestHelper.getRequestListByAid(recipientId)
    if(result != None):
      for row in result:
        requestList.append({'sender_id':row[0],'name':row[2],'time':str(row[1]),'nick_name':row[3],'server_name':row[4]})

      return json.dumps(requestList)
    else:
      return None
  '''
    Get request count by author id
  '''
  def getRequestCountByAid(self,recipientId):
 
    result = self.requestHelper.getRequestCountByAid(recipientId)

    if(result != None):
      if(result != 0):
        return json.dumps({'count':result})
      else:
        return json.dumps({'count':0})
    else:
      return None
  def deleteAllRequestByAid(self,recipientId):
    """
    To delete all requests by reciever
    """
    return self.requestHelper.deleteAllRequestByAid(recipientId)
  def getSentRequest(self,sender_id):
    """
    get a list of aid,which belongs to the author the sender sent
    """
    cur =  self.requestHelper.getSentRequestByAid(sender_id)
    if cur == None:
      return cur
    re = []
    for row in cur:
      re.append(row[0])
    return re


