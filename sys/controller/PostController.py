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
    Get local public posts
    '''
    def getLocalPublicPosts(self):

        rows = self.posthelper.getLocalPublicPosts()
        if rows != None:
            postsArray = []
            for row in rows:
                post = {}
                author = {}
                author['id'] = row[6]
                author['host'] = row[8]
                author['displayname'] = row[7]
                author['url'] = ""

                post['title'] = row[2]
                post['source'] = ""
                post['origin'] = ""
                post['description'] = ""
                post['content-type'] = row[4]
                post['content'] = row[3]
                post['guid'] = row[0]
                post['categories'] = ""
                post['pubDate'] = row[1].strftime("%Y-%m-%d %H:%M:%S")
                post['visibility'] = row[5]
                post['author'] = author
                post['comments'] = []
                
                postsArray.append(post)
            return postsArray
        return None
    '''
      get post by author id
    '''
    def getPostByAid(self,aid):
        list = self.posthelper.getPostByAid(aid)
        if list == None:
            return None
        re =[]
        for post in list:
            re.append(post.tojson())
        return json.dumps(re)
    '''
      get post by myself
    '''    
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
