from PostHelper import *
import json
import sys
class PostController:
    """
        to initial an instance of posthelper
        
    """
    def __init__(self,dbAdapter):
        self.posthelper = PostHelper(dbAdapter)
    """
        Get json file of all post, which the author can see
        @param aid author id
        @return None
        @return jsonstring
    """
    def getPost(self,aid):
        post_list=[]
        json_list={}
        post_list.extend(self.posthelper.getPublicPost(aid))
        post_list.extend(self.posthelper.getPrivatePost(aid))
        post_list.extend(self.posthelper.getFriendsFriendPost(aid))
        post_list.extend(self.posthelper.getFriendsPost(aid))
        post_list.extend(self.posthelper.getAuthorPost(aid))
        post_list.extend(self.posthelper.getMyHostFriendPost(aid))
        post_list.extend(self.posthelper.getSelectedPost(aid))
        for post in post_list:
            if(post is None):
                return None
            else:
                json_list[post.getPid()]=post.tojson()
        return json.dumps(json_list)
