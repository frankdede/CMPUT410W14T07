
import json
import flask
from flask import Flask, request, redirect, url_for, g, render_template, flash, session, abort,make_response
import sys,os
sys.path.append('sys/controller')
sys.path.append('sys/model')
from authorhelper import *
from posthelper import *
from databasehelper import *
#from requesthelper import *
from circlehelper import *

DEBUG = True
# create a new database obj
dbHelper = Databasehelper()
# connect
dbHelper.connect()
dbHelper.setAutoCommit()

ahelper = AuthorHelper(dbHelper)
# use the conneted dbHelper to initialize postHelper obj
postHelper = PostHelper(dbHelper)
# 
#reHelper = RequetHelper(dbHelper)
#
circleHelper = CircleHelper(dbHelper)

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = os.urandom(24)
error = None

def flaskPostToJson():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data != ''):
        return json.loads(request.data)
    else:
        return json.loads(request.form.keys()[0])

# default path
@app.route('/', methods=['GET', 'POST'])
def root():
        #username = session['logged_in']
        #mumMsg = reHelper.getMessageCountByAuthorName(username)
    return render_template('addfriend.html')
if __name__ == '__main__':
    app.debug = True
    app.run()
