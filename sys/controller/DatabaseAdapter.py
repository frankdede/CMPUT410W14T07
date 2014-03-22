import mysql.connector
#read name and password from information file
class DatabaseAdapter:
    def __init__(self):
        self.cnx = None
    def readpassword(self):
        try:
            f = open('information','r')
            list = f.read(256)
            name = list.split(',')[0]
            password = list.split(',')[1]
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except ValueError:
            print "Could not convert data to an integer."
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        return name,password
#create connection to database
    def connect(self):
        from mysql.connector import errorcode
        name =""
        password=""
        name,password = self.readpassword() 
        try:
            self.cnx = mysql.connector.connect(user=name, password=password,host='127.0.0.1',database='c410')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exists")
            else:
                print(err)
# get dabase connector


    def executeFetchStmt():


    def executeUpdateStmt():




    def setAutoCommit(self):
        self.cnx.autocommit = True
    def getdabaseconnector(self):
        return self.cnx
    def commit(self):
        self.cnx.commit()
# close current connection
    def close(self):
        self.cnx.close()
# return cursor of database
    def isconnect(self):
        return self.cnx !=  None
    def getcursor(self):
        return self.cnx.cursor()
if __name__ == "__main__":
    databasehelper = Databasehelper()
    databasehelper.connect()
