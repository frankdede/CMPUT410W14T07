from CommentHelper import *
import sys
sys.path.append("sys/model")
from comment import *

class CommentController:

    def __init__(self,dbAdapter):
        self.commentHelper = CommentHelper(dbAdapter)

    '''
    Get all comments for a specific post by its id
    @param String Post ID
    @return String/None Returns a JSON formatted dictionary of comments if getting successfully, else None
    '''
    def getAllCommentsForPost(self,pid):
        
        result = self.commentHelper.getAllCommentsForPost(pid)
        if result != None:
            commentDict = {}
            for item in result:
                comment = Comment(item['cid'],item['aid'],item['nick_name'],item['time'],item['content'])
                commentDict[comment.getCid()] = comment.tojson()
            return json.dumps(commentDict)
        return None
    '''
    Add comment for a specific post 
    @param String Author ID
    @param String Post ID
    @param String Content
    @return String/Boolean Returns Aid if adding successfully, else False
    '''
    def addCommentForPost(self,aid,pid,content):

        return self.commentHelper.addCommentForPost(aid,pid,content)

    '''
    Delete comment for a specific post
    @param String Comment ID
    @return Boolean
    '''
    def deleteCommentForPost(self,cid):

        return self.commentHelper.deleteCommentForPost(cid)
    '''
    Count number of comments for a specific post
    '''
    def countCommentsForPost(self,pid):

        return self.commentHelper.countCommentsForPost(pid)