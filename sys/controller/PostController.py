from PostHelper import *
import json
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
        try:
            post_list.extend(self.posthelper.getPublicPost())
            post_list.extend(self.posthelper.getPrivatePost())
            post_list.extend(self.posthelper.getFriendsFriendPost())
            post_list.extend(self.posthelper.getFriendsPost())
            post_list.extend(self.posthelper.getAuthorPost())
            post_list.extend(self.posthelper.getMyHostFriendPost())
        except TypeError:
            return None
        json_list=[]
        for i in post_list:
            if(i is None):
                return None
            else:
                json_list.append(i.tojson())
        return json.dumps(json_list)