from AuthorHelper import *
from DatabaseAdapter import *
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
        for author in tmp_list:
            current_aid =author.getAid()
            if current_aid !=aid:
                dic['aid'] = current_aid
                dic['name'] = author.getName()
                dic['nickname'] = author.getNickname()
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
    def searchAuthorByString(self,keyword):
        """
            To search keyword inside a row string
            """
        list = Utility.parseKeyword(keyword)
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
                re.append(dic)
                dic ={}
            return json.dumps(re)
        return None
    def getAuthorByAid(self,aid):
        """
            To get author json by aid
        """
        author = self.authorHelper.getAuthorObjectByAid(aid)
        if author !=None:
            return json.dumps(author.tojson())
        else:
            return False

    def addRemoteAuthor(self,aid,displayName,sid):
        
        return self.authorHelper.addRemoteAuthor(aid,displayName,sid)

    def addAuthor(self,name,password,nickName,sid='cs410.cs.ualberta.ca:41070'):

        return self.authorHelper.addAuthor(name,password,nickName,sid)

    def getAllTmpAuthor(self):
        re = []
        list = self.authorHelper.getAllTmpAuthorObjects()
        if list !=None:
            for author in list:
                re.append(author.tojson())
            return json.dumps(re)
        else:
            return None