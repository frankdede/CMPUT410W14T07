import json
import flask
import markdown
from flask import Flask, request, redirect, url_for, g, render_template, flash, session, abort,make_response, Markup
from werkzeug.utils import secure_filename
from random import randrange
import sys,os
import binascii
from rauth import OAuth2Service
sys.path.append('sys/controller')
sys.path.append('sys/model')
from AuthorHelper import *
from DatabaseAdapter import *

from RequestHelper import *
from CircleHelper import *
from PostController import *
from AuthorController import *
from RequestController import *
DEBUG = True
# create a new database obj
dbAdapter = DatabaseAdapter()
# connect
dbAdapter.connect()
dbAdapter.setAutoCommit()

ahelper = AuthorHelper(dbAdapter)
aController = AuthorController(dbAdapter)
# use the conneted dbAdapter to initialize postHelper obj
postcontroller = PostController(dbAdapter)
#
reController = RequestController(dbAdapter)
#
circleHelper = CircleHelper(dbAdapter)
#Allowed file extensions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config.from_object(__name__)
# add upload
UPLOAD_FOLDER='upload/image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)
error = None
GITHUB_CLIENT_ID = '02b57f045e11c12db42c'
GITHUB_CLIENT_SECRET = 'b759b58460b2f81cfef696f7bf157be9460517f2'
github = OAuth2Service(
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET,
    name='github',
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    base_url='https://api.github.com/')

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
    return redirect(url_for('login'))
@app.route('/<aid>', methods=['GET', 'POST'])
def author_view(aid):
    if 'logged_in' in session:
        if(session['logged_id']==aid):
            username = session['logged_in']
            msgCount = reController.getRequestCountByAid(aid)
            countnumber = json.loads(msgCount)['count']
            return render_template('header.html',msgCount = countnumber)
    else:
        return redirect(url_for('login'))
@app.route('/ajax/aid')
def getuid():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        re = make_response(session['logged_id'])
        re.headers['Content-Type']='text/plain'
        return re
@app.route('/ajax/author_name')
def getaname():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
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
        json_str = ahelper.authorAuthenticate(authorName,password)
        if  json_str == False:
            re = make_response("False")
            re.headers['Content-Type']='text/plain'
            return re
        else:
            session['logged_in'] = authorName
            session['logged_id'] = json.loads(json_str)['aid']
            return json_str
    else:
        if not session.get('oauth_state'):
            session['oauth_state'] = binascii.hexlify(os.urandom(24))
        authorize_url = github.get_authorize_url(scope='user,notifications', state=session.get('oauth_state'))
        return render_template('header.html',authorize_url=authorize_url)
    if "logged_in" in session:
        aid = session['logged_id']
        msgCount = reController.getRequestCountByAid(aid)
        countnumber = json.loads(msgCount)['count']
        return render_template('header.html',msgCount = countnumber)
    else:
        return render_template('header.html')

# register page
@app.route('/register', methods=['PUT', 'POST'])
def register():
    if request.method == 'POST':
        #parse require information
        gender=""
        email = request.form['email']
        authorName=request.form['author_name']
        password=request.form['register_pwd']
        #parse optional information
        file = request.files['profile_image']
        nickName=request.form['nick_name']
        birthday =request.form['birthday']
        city = request.form['city']
        try:
            gender = request.form['gender']
        except KeyError:
            gender = ""
        aid_json = ahelper.addAuthor(authorName,password,nickName)
        if aid_json == False:
            re = make_response("False")
            re.headers['Content-Type']='text/plain'
            return re
        else:
            aid = json.loads(aid_json)['aid']
            session['logged_in'] = authorName
            session['logged_id'] = aid
            if(file!=None or file.name!=""):
                save_image(aid,file)
            if ahelper.updateAuthorInfo(aid,email,gender,city,birthday,path) ==False:
                abort(500)
            return aid_json
    return redirect(url_for('/'))
def save_image(aid,file):
    filename = aid+file.name.rsplit('.', 1)[1]
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
@app.route('/<aid>/recommended_authorlist.json', methods=['GET'])
def authorlist(aid):
    if ('logged_in' not in session) or (aid !=session['logged_id']):
        abort(404)
    re = aController.getRecommendedAuthor(aid)
    return re
@app.route('/<aid>/authorlist.json',methods=['GET'])
def allauthorlist(aid):
    if ('logged_in' not in session) or (aid !=session['logged_id']):
        return redirect(url_for('/'))
    re = aController.getOtherAuthor(aid)
    print re
    return re
@app.route('/messages.json', methods=['GET'])
def messages(authorName):
    if ('logged_in' not in session) or (authorName !=session['logged_in']):
        abort(404)
    else:
        jsonstring = reController.getRequestListByAid(aid)
        return jsonstring,200

# logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))
# make request
@app.route('/<aid>/author/request',methods=['GET'])
def addfriend(aid):
    if ('logged_in' not in session) or (session['logged_id'] != aid):
        abort(400)
    else:
        try:
            request_aid = request.args.get('recipient')
            if reController.sendRequest(aid,request_aid) is True:
                re = make_response("OK")
                return re
            else:
                re = make_response("Existed")
                return re
        except KeyError:
            return redirect(url_for(aid))
@app.route('/author/<authorName>')
def renderStruct(authorName):

    if ('logged_in' in session) and (session['logged_in'] == authorName):
        return render_template('struct.html')
    else:
        return abort(404)

# get all the new posts that a specific author can view from the server
@app.route('/<authorName>/pull/')
def getUpdatedPost(authorName):

    if ('logged_in' in session) and (session['logged_in'] == authorName):
        aid = session['logged_id']
        if aid == None:
            return json.dumps({'status':None}),200
        else:    
            post = postcontroller.getPost(aid)
            print post
            return post,200
    else:
        return abort(404)

@app.route('/markdown',methods=['GET','POST'])

def index():
    if request.method == 'POST':
        content = request.form['postMarkDown']
        print content
        content = Markup(markdown.markdown(content))
        return render_template('markdown.html', **locals())
    return render_template('markdown_input.html')


@app.route('/<authorName>/post/',methods=['PUT','POST'])
def uploadPostToServer(authorName):

    if ('logged_in' in session) and (session['logged_in'] == authorName):

        aid = ahelper.getAidByAuthorName(authorName)

        postObj = flaskPostToJson()
        postTitle = postObj['title']
        postMsg = postObj['message']
        postType = postObj['type']
        postPermission = postObj['permission']

        if aid == None:
            return json.dumps({'status':False}),200
        else:
            newPost = Post(None,aid,None,postTitle,postMsg,postType,postPermission)
            result = postHelper.addPost(newPost)
        return json.dumps({'status':result}),200
    else:
        return abort(404)

# This is used to get friend list from database
@app.route('/<authorName>/post/getPermissionList/',methods=['GET'])
def getPermissionList(authorName):

    if ('logged_in' in session) and (session['logged_in'] == authorName):
        if request.method == 'GET':
            # Get the permission: friend or fof, from parameter 
            permission = request.args.get('option')

            if permission == "friend" or permission == "friends":
                friendlist = circleHelper.getFriendList(authorName)
                if friendlist != None:
                    return json.dumps(friendlist),200

                elif permission == "fof":
                    fof = circleHelper.getFriendOfFriend(authorName)

                    if fof != None:
                        return json.dumps(fof),200
                    else:
                        return "null",200
                        return "null",200
    else:
        return abort(404)

# get all the new posts that a specific author can view from the server
@app.route('/<authorName>/github/notification')
def getNotification(authorName):
    if ('logged_in' in session) and (session['logged_in'] == authorName):
        # get author auth token
        authorToken = authorName + '_authToken'
        authorAuthToken=session[authorToken]
        # get auth session
        auth_session = github.get_session(token=authorAuthToken)
        aid = session['logged_id']
        if aid == None:
            return json.dumps({'status':None}),200
        else:    
            r = auth_session.get('/notifications')
            for i in range(0,len(r.json())):
                postMsg=''
                for key,value in r.json()[i].iteritems():
                    if key == "updated_at":
                        postMsg=postMsg+"updatet time: " + value +"\n"
                        print "updatet time: " + value
                    elif key == "subject":
                        for key1,value1 in value.iteritems():
                            if key1 == "url":
                                postMsg=postMsg+"update at: " + value1 +"\n"
                                print "update at: " + value1
                            elif key1 == "title":
                                postMsg=postMsg+"title :" + value1 +"\n"
                                print "title :" + value1
                #newPost = Post(None,aid,None,'Github Notification',postMsg,'text','me')
                #result = postHelper.addPost(aid,'Github Notification',postMsg,'text','me')
        r = auth_session.put('/notifications')
        return "a"
    else:
        return abort(404)

@app.route('/github/callback')
def callback():
    code = request.args['code']
    state = request.args['state'].encode('utf-8')
    #if state!=session.get('oauth_state'):
        #return render_template('header.html')
    # get auth session
    auth_session = github.get_auth_session(data={'code': code})
    # get author name
    r = auth_session.get('/user')
    authorName = r.json()['login']
    # store author token
    authorToken = authorName + '_authToken'
    session[authorToken] = auth_session.access_token
    # try to register account
    aid_json = ahelper.addAuthor(authorName,123,authorName)
    if aid_json!= False:
        aid = json.loads(aid_json)['aid']
        session['logged_in'] = authorName
        session['logged_id'] = aid   
    else:
        # try to log in
        json_str = ahelper.authorAuthenticate(authorName,123)
        if json_str!=False:
            session['logged_in'] = authorName
            session['logged_id'] = json.loads(json_str)['aid']
        else:
            re = make_response("False")
            re.headers['Content-Type']='text/plain'
            return re
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
