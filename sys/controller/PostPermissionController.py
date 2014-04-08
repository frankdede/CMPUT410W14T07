import json
from PostPermissionHelper import *
class PostPermissionController:
    def __init__(self,dbAdapter):
        self.postPermissionHelper = PostPermissionHelper(dbAdapter)

    '''add post permission to post'''
    def addPostPermission(self,pid,aidList):
        return self.postPermissionHelper.addPostPermission(pid,aidList)
