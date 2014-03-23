import mysql.connector
import Utility
from DatabaseAdapter import *

class CommentHelper:
	def __init__(self,dbAdapter):
		self.dbAdapter = dbAdapter

	#Get all the comments for a specific post
	def getAllCommentsForPost(postId):

		cur = self.dbAdapter.getcursor()
		query = ("SELECT C.pid,"
				"C.cid,"
				"A.name,"
				"A.nick_name,"
				"C.content,"
				"C.time "
				"FROM author A, comments C "
				"WHERE C.pid = %s;")%(postId)
		try:
			cur.execute(query)

		except mysql.connector.Error as err:

			print("****************************************")
            print("SQLException from getAllCommentsForPost():")
            print("Error code:", err.errno)
            print("SQLSTATE value:", err.sqlstate)
            print("Error message:", err.msg)
            print("Might be query issue:",query)
            print("****************************************")
            return None
    	if cur.rowcount > 0:
    		return cur.fetchall()   
    	return None 

	#Add a comment to a specific post
	def addCommentForPost(aid,pid,content):

		cid = Utility.getid()
		cur = self.dbApdater.getcursor()
		query = ("INSERT INTO comments"
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

	def deleteCommentForPost(cid):
		 

	def countCommentsForPost(pid):

		cur = self.dbAdapter.getcursor()
		query = ("SELECT pid,count(*) FROM ")




