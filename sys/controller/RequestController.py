import mysql.connector
from CircleController import *
from RequestHelper import *
import json

class RequestController:

  def __init__(self,dbAdapter):
    self.requestHelper = RequestHelper(dbAdapter)
    self.circleController = CircleController(dbAdapter)

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
    result = getRequestListByAid(recipientId)
    print(result)
    if(result != None):
      for row in result:
                requestList.append({'sender_id':row[0],'time':str(row[1])})

      return json.dumps(requestList)
    else:
      return None

  def getRequestCountByAid(self,recipientId):

    result = self.requestHelper.getRequestCountByAid(recipientId)

    if(result != None):
      if(result != 0):
        return json.dumps({'count':result})
      else:
        return json.dumps({'count':0})
    else:
      return None



    

