from CommentHelper import *

class CommentController:
    commentHelper = None
    def __init__(self,dbAdapter):
        self.commentHelper = CommentHelper(dbAdapter)

    def getAllCommentsForPost(self,pid):
         result = self.commentHelper.getAllCommentsForPost(pid)

         for comment in result 

