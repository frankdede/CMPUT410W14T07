'''this is data base setup file'''

USER = str(raw_input("Mysql username:"))
PASS = str(raw_input("Password:"))
f = open('information', 'w')
f.write(USER+","+PASS)
