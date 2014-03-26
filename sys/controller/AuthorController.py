from AuthorHelper import *
from DatabaseAdapter import *
import sys
sys.path.append("sys/model")
import json
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