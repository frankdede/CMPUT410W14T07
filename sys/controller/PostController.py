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


        publicPost = self.posthelper.getPublicPost(aid)
        if publicPost != None:
            post_list.extend(publicPost)

        privatePost = self.posthelper.getPrivatePost(aid)
        if privatePost != None:
            post_list.extend(privatePost)

        fofPost = self.posthelper.getFriendsFriendPost(aid)
        if fofPost != None:
            post_list.extend(fofPost)

        friendsPost = self.posthelper.getFriendsPost(aid)
        if friendsPost != None:
            post_list.extend(friendsPost)

        authorPost = self.posthelper.getAuthorPost(aid)
        if authorPost != None:
            post_list.extend(authorPost)

        myHostFriendPost = self.posthelper.getMyHostFriendPost(aid)
        if myHostFriendPost != None:
            post_list.extend(myHostFriendPost)

        selectedPost = self.posthelper.getSelectedPost(aid)
        if selectedPost != None:
            post_list.extend(selectedPost)

        for post in post_list:
            if(post is None):
                return None
            else:
                json_list[post.getPid()]=post.tojson()
        return json.dumps(json_list)
    '''
    For public API to use only
    '''
    def getLocalPublicPosts(self):

        posts = self.posthelper.getLocalPublicPosts()





    def getPostByAid(self,aid):
        list = self.posthelper.getPostByAid(aid)
        if list == None:
            return None
        re =[]
        for post in list:
            re.append(post.tojson())
        return json.dumps(re)
        
    def getMyPost(self,aid):
        post_list=[]
        json_list={}
        post_list.extend(self.posthelper.getMyPost(aid))
        for post in post_list:
            if(post is None):
                return None
            else:
                json_list[post.getPid()]=post.tojson()
        return json.dumps(json_list)
