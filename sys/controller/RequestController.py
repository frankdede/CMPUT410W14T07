import mysql.connector
from CircleController import *
from RequestHelper import *
import json

class RequestController:
  '''
    An instance of RequestHelper Class
  '''
  requestHelper = None

  '''
    An instance of RequestHelper Class
  '''
  circleController = None

  def __init__(self,dbAdapter):
    self.requestHelper = RequestHelper(dbAdapter)
    self.circleController = CircleController(dbAdapter)

  def accpetRequestFromSender(self,recipientId,senderId):

    result = self.circleController.addFriendForAuthor(recipientId,senderId)
    if (result == True):
       return self.deleteRequest(recipientId,senderId)

    return False

  '''
    @param String senderId
    @param String recipientId
    @return Boolean 
  '''
  def sendRequest(self,senderId,recipientId):

    return  addNewRequest(self,recipientId,senderId)

  '''
    Delete a request by recipient ID and sender ID
    @param String senderId
    @param String recipientId
    @return Boolean 
  '''
  def deleteRequest(self,recipientId,senderId):

    return  deleteRequest(recipientId,senderId)

  '''
    Get all the requests content based on recipient ID
    @param String recipientId
    @return String JSON String 
  '''
  def getAllRequestByAid(self,recipientId):

    requestList = []
    result = getRequestListByAid(recipientId)

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
        return json.dumps({'count':row[0]})
      else:
        return json.dumps({'count':0})
    else:
      return None



    

