import mysql.connector
import Utility
from DatabaseAdapter import *

class CommentHelper:
    def __init__(self,dbAdapter):
        self.dbAdapter = dbAdapter


    '''get all comments by author id'''
    def getCommentsForAuthor(self,aid):

        cur = self.dbAdapter.getcursor()
        query =("SELECT "
                "C.cid,"
                "C.aid,"
                "A.nick_name,"
                "C.content,"
                "C.time,"
                "C.pid "
                "FROM author A, comments C "
                "WHERE A.aid = C.aid AND C.aid = '%s';")%(aid)
        try:
            cur.execute(query)
        except mysql.connector.Error as err:

            print("****************************************")
            print("SQLException from getCommentsForAuthor():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return None

        return cur.fetchall()

    #Get all the comments for a specific post
    def getCommentsForPost(self,pid):

        cur = self.dbAdapter.getcursor()

        query = ("SELECT "
                "C.cid,"
                "C.aid,"
                "A.nick_name,"
                "C.content,"
                "C.time "
                "FROM author A, comments C "
                "WHERE C.pid = '%s' AND C.aid = A.aid;")%(pid)
        try:
            cur.execute(query)

        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from getCommentsForPost():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return None

        return cur.fetchall()


    '''get all comments for public posts'''
    def getCommentsForPublicPosts(self):

        cur = self.dbAdapter.getcursor()

        query = ("SELECT "
                "C.cid,"
                "C.aid,"
                "A.nick_name,"
                "C.content,"
                "C.time,"
                "S.url,"
                "C.pid "
                "FROM author A, comments C, servers S, post P "
                "WHERE P.permission = 'public' AND P.pid = C.pid "
                "AND C.aid = A.aid AND A.sid = S.sid AND S.local = 1;")
        try:
            cur.execute(query)

        except mysql.connector.Error as err:
            print("****************************************")
            print("SQLException from getCommentForPublicPosts():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return None

        return cur.fetchall()

    '''Add a comment to a specific post'''
    def addCommentForPost(self,aid,pid,content):

        cid = Utility.getid()
        cur = self.dbAdapter.getcursor()
        query = ("INSERT INTO comments "
                "VALUES('%s','%s','%s',NULL,'%s')")%(cid,pid,aid,content)

        try:
            cur.execute(query)

        except mysql.connector.Error as err:

            print("****************************************")
            print("SQLException from addCommentForPost():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return None
        if cur.rowcount > 0:
            return cid
        return False


    '''delete comments for a post'''
    def deleteCommentForPost(self,cid):

        cur = self.dbAdapter.getcursor()
        query = ("DELETE FROM comments WHERE cid = '%s' ")%(cid)

        try:
            cur.execute(query)

        except mysql.connector.Error as err:

            print("****************************************")
            print("SQLException from deleteCommentForPost():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return False
        return cur.rowcount > 0

    ''' count comments for a post'''
    def countCommentsForPost(self,pid):

        cur = self.dbAdapter.getcursor()
        query = ("SELECT count(*) FROM comments where pid = '%s'") %(pid)

        try:
            cur.execute(query)

        except mysql.connector.Error as err:

            print("****************************************")
            print("SQLException from countCommentsForPost():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return None
        return cur.rowcount
