
import json
import flask
from flask import Flask, request, redirect, url_for, g, render_template, flash, session, abort,make_response
import sys,os
sys.path.append('sys/controller')
sys.path.append('sys/model')
from authorhelper import *
from posthelper import *
from databasehelper import *
from messagehelper import *

DEBUG = True
# create a new database obj
dbHelper = Databasehelper()
# connect
dbHelper.connect()

ahelper = AuthorHelper(dbHelper)
# use the conneted dbHelper to initialize postHelper obj
postHelper = PostHelper(dbHelper)
msgHelper = Messagehelper(dbHelper)

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = os.urandom(24)
error = None

# default path
@app.route('/', methods=['GET', 'POST'])
def root():
    if 'logged_in' in session:
        username = session['logged_in']
        mumMsg = msgHelper.getMessageCountByAuthorName(username)
        return render_template('header.html')
    else:
        return redirect(url_for('login'))
@app.route('/ajax/uid')
def getuid():
    if 'logged_in' not in session:
        abort(404)
    else:
        re = make_response(session['logged_in'])
        re.headers['Content-Type']='text/plain'
        return re
# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        authorName =request.form['username']
        password =request.form['password']
        if ahelper.authorAuthenticate(authorName,password):
            session['logged_in'] = authorName
            error="login successful"
            re = make_response("True")
            re.headers['Content-Type']='text/plain'
            return re
        else:
            re = make_response("False")
            re.headers['Content-Type']='text/plain'
            return re
    return render_template('header.html')

# register page

@app.route('/register', methods=['PUT', 'POST'])
def register():
    if request.method == 'POST':
        authorName=request.form['username']
        password=request.form['password']
        nickName=request.form['nick_name']
        if ahelper.addAuthor(authorName,password,nickName):
            re = make_response("True")
            session['logged_in'] = authorName
            re.headers['Content-Type']='text/plain'
            return re
        else:
            re = make_response("False")
            re.headers['Content-Type']='text/plain'
            return re
    return redirect(url_for('/'))


@app.route('/<authorName>/messages.json', methods=['GET'])
def messages(authorName):
    if ('logged_in' not in session) or (authorName !=session['logged_in']):
        abort(404)
    else:
        jsonstring = msghelper.getUnreadMessageListByAuthorName(username)
        return jsonstring,200

# logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/author/<authorName>')
def renderStruct(authorName):

    if ('logged_in' in session) and (session['logged_in'] == authorName):
        return render_template('struct.html')
    else:
        return redirect('/templates/error/404.html'),404;

# get all the new posts that a specific author can view from the server
@app.route('/pull/<authorName>')
def getUpdatedPost(authorName):

    if ('logged_in' in session) and (session['logged_in'] == authorName):
        aid = ahelper.getAidByAuthorName(authorName)

        if aid == None:
            return json.dumps({'aid':None}),200
        else:    
            post = postHelper.getPostList(aid)
            return post,200
    else:
         return redirect('/templates/error/404.html'),404

@app.route('/post/<authorName>',methods=['PUT','POST'])
def uploadPostToServer(authorName):

    if ('logged_in' in session) and (session['logged_in'] == authorName):

        aid = ahelper.getAidByAuthorName(authorName)
        msg = request.form['message']
        permission = request.form['permission']
        msgType = request.form['type']

        if aid == None:
            return json.dumps({'aid':False}),200
        else:
            newPost = Post(None,aid,None,'',msg,msgType,permission)
            result = postHelper.addPost(newPost)
            return json.dumps({'aid':result}),200
        
if __name__ == '__main__':
    app.debug = True
    app.run()
