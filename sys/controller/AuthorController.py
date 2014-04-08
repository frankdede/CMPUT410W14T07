from AuthorHelper import *
from RequestController import *
from CircleController import *
from DatabaseAdapter import *
from ServerHelper import *
import sys
sys.path.append("sys/model")
import json
import Utility
class AuthorController:
    """
        Author Contoller is used to control author helper
    """
    def __init__(self,dbAdapter):
        self.authorHelper = AuthorHelper(dbAdapter)
        self.requestController = RequestController(dbAdapter)
        self.serverHelper = ServerHelper(dbAdapter)
        self.circleController = CircleController(dbAdapter)
    def getOtherAuthor(self,aid):
        """
            to get list of authors except for the author by aid
            @param: aid
            @return jsonstring with name and aid
            """
        dic = {}
        re = []
        tmp_list =self.authorHelper.getAllAuthorObjectsForLocalServer()
        tmp_list.extend(self.authorHelper.getAllAuthorObjectsForRemoteServer())
        sent_list = self.requestController.getSentRequest(aid)
        for author in tmp_list:
            current_aid =author.getAid()
            if current_aid !=aid:
                dic['aid'] = current_aid
                dic['name'] = author.getName()
                dic['nickname'] = author.getNickname()
                dic['server_name'] = self.serverHelper.getServerNameBySid(author.getSid())
                if current_aid in sent_list:
                    dic['followed'] = 1
                else:
                    dic['followed'] = 0
                re.append(dic)
                dic ={}
        return json.dumps(re)
    def getRecommendedAuthor(self,aid):
        """
            to get list of recommended authors
            @param: aid
            @return: jsonstring with name and aid
            """
        tmp_list =self.authorHelper.getRecommendedAuthorList(aid)
        return json.dumps(tmp_list)
    def searchAuthorByString(self,aid,keyword):
        """
            To search keyword inside a row string
            """
        list = Utility.parseKeyword(keyword)
        sent_list = self.requestController.getSentRequest(aid)
        firend_list = self.circleController.getFriendAidList(aid)
        print firend_list
        re =[]
        tmp_list =[]
        dic = {}
        if(list!=None):
            for i in list:
                tmp_list.extend(self.authorHelper.searchAuthor(i))
            for author in tmp_list:
                current_aid =author.getAid()
                dic['aid'] = current_aid
                dic['name'] = author.getName()
                dic['nickname'] = author.getNickname()
                dic['server_name'] = self.serverHelper.getServerNameBySid(author.getSid())
                if current_aid in sent_list:
                    dic['followed'] = 1
                else:
                    dic['followed'] = 0
                if current_aid in firend_list:
                    dic['firend'] = 1
                else:
                    dic['friend'] = 0
                re.append(dic)
                dic ={}
            return json.dumps(re)
        return None

    '''
    Get an jsonified author object by aid
    '''
    def getAuthorByAid(self,aid):
       
        author = self.authorHelper.getAuthorObjectByAid(aid)
        if author != None:
            return json.dumps(author.tojson())
        else:
            return None

    '''
    Get an author object by aid
    '''
    def getAuthorInfoByAid(self,aid):
        author = self.authorHelper.getAuthorObjectByAid(aid)
        if author != None:
            return author
        else:
            return None
    '''
    Add a remote author into database
    '''
    def addRemoteAuthor(self,aid,displayName,sid):
        
        return self.authorHelper.addRemoteAuthor(aid,displayName,sid)

    '''
    Add a local author into database
    '''
    def addAuthor(self,name,password,nickName,sid='cs410.cs.ualberta.ca:41070'):

        return self.authorHelper.addAuthor(name,password,nickName,sid)
    '''
    Get all temp authors
    '''
    def getAllTmpAuthor(self):
        re = []
        list = self.authorHelper.getAllTmpAuthorObjects()
        if list !=None:
            for author in list:
                re.append(author.tojson())
            return json.dumps(re)
        else:
            return None
    '''
    check whether the author is remote or not
    '''
    def isRemoteAuthor(self,aid):
        
        return self.authorHelper.isRemoteAuthor(aid)
    '''
    get all global authors
    '''

    def getGlobalAuthors(self):

        rows = self.authorHelper.getGlobalAuthors()
        if(rows != None):
            authors = []
            for row in rows:
                author = {}
                author['id'] = row[0]
                author['displayname'] = row[1]
                authors.append(author)
                
            return authors
        else:
            return None
    '''
    check whether the author exists or not
    '''
    def doesAuthorExists(self,aid):

        return self.authorHelper.doesAuthorExists(aid)

