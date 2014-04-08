import json

import flask
import requests
import markdown
import httplib

from time import gmtime, strftime
from flask import Flask, request, redirect, url_for, g, render_template, flash, session
from flask import abort,make_response, Markup, send_from_directory,send_file
from werkzeug.utils import secure_filename

from random import randrange
import sys,os
from mimetypes import MimeTypes
import urllib
import binascii
from rauth import OAuth2Service
sys.path.append('sys/controller')
sys.path.append('sys/model')

# import all helpers
from AuthorHelper import *
from DatabaseAdapter import *
from PostHelper import *
from RequestHelper import *
from CircleHelper import *
from SettingHelper import *
# import all controllers
from PostController import *
from AuthorController import *
from RequestController import *
from CommentController import *
from ServiceController import *
from ServerController import *
from PostPermissionController import *
from ImageHelper import *

DEBUG = True
# create a new database obj
dbAdapter = DatabaseAdapter()
# connect
dbAdapter.connect()
dbAdapter.setAutoCommit()

ahelper = AuthorHelper(dbAdapter)
aController = AuthorController(dbAdapter)
# use the conneted dbAdapter to initialize postHelper obj
postHelper = PostHelper(dbAdapter)
postController = PostController(dbAdapter)
#
reController = RequestController(dbAdapter)
#
circleHelper = CircleHelper(dbAdapter)
circleController = CircleController(dbAdapter)
#
commentController = CommentController(dbAdapter)
settingHelper = SettingHelper(dbAdapter)
#
serviceController = ServiceController(dbAdapter)
#
postPermissionHelper = PostPermissionController(dbAdapter)
#
serverController = ServerController(dbAdapter)

imageHelper = ImageHelper(dbAdapter)
#Allowed file extensions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config.from_object(__name__)
REGISTER_RESTRICTION = None
POST_REMOTE_ACCESS_RESTRICTION = None
IMAGE_REMOTE_ACCESS_RESTRICTION = None
# add upload
UPLOAD_FOLDER='upload/image'
PERMISSION_IMAGE='static/image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.secret_key = os.urandom(24)
admin_id = '000000'
admin_name='admin'
admin_model = False
error = None

'''git connection'''

GITHUB_CLIENT_ID = '5a4bdc64c247e1f45f61'
GITHUB_CLIENT_SECRET = '0640b9e5a32d2ebe6f4713158f2321f8ac43cee4'

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
    '''direct for login'''

    return redirect(url_for('login'))

@app.route('/<aid>', methods=['GET', 'POST'])
def author_view(aid):
    '''header view'''

    if 'logged_in' in session and aid ==session['logged_id']:
        username = session['logged_in']
        msgCount = reController.getRequestCountByAid(aid)
        countnumber = json.loads(msgCount)['count']
        return render_template('header.html',msgCount = countnumber)
    else:
        return redirect(url_for('login'))

@app.route('/<aid>/profile',methods=['GET'])
def view_profile(aid):
    '''return a html for profile'''

    return render_template('profile.html')

@app.route('/<aid>/profile/image/<imagename>',methods=['GET'])
def view_profile_image(aid,imagename):
    '''load the profile image'''

    #print imagename
    import os.path
    path = os.path.join(app.config['UPLOAD_FOLDER'],imagename);
    print os.path.isfile(path)
    if os.path.isfile(path):
        return send_from_directory(app.config['UPLOAD_FOLDER'],imagename, as_attachment=False)
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'],"default.jpeg", as_attachment=False)
@app.route('/<aid>/profile.json',methods=['GET'])
def get_profile(aid):
    '''return author profile'''

    if 'logged_in' in session and aid ==session['logged_id']:
        try:
            re_aid = request.args.get("aid")
            print re_aid
            re = aController.getAuthorByAid(re_aid)
            if re != None:
                return re
            return redirect(url_for('/'))
        except KeyError:
            return redirect(url_for('/'))
    return redirect(url_for('/'))
    
@app.route('/<aid>/profile/change',methods=['POST'])
def change_profile(aid):
    '''redirect after update profile change'''

    if 'logged_in' in session and aid ==session['logged_id']:
        return change_author_profile(aid)
    else:
        return redirect(url_for('/'))

def change_author_profile(aid):
    '''update profile change'''
    try:
        keyword = request.args.get('type')
        print keyword
    except KeyError:
        return "Wrong URL",404
    if keyword == "information":
        gender=""
        filename=""
        email = request.form['email']
        #parse optional information
        nickName=request.form['nick_name']
        birthday =request.form['birthday']
        city = request.form['city']
        try:
            file = request.files['profile_image']
            filename = file.filename
            #print "--"+file.filename
        except KeyError:
            file =None
        try:
            gender = request.form['gender']
        except KeyError:
            gender = ""
        if file!=None and filename!="":
            filename = save_image(aid,file)
        if ahelper.updateAuthorInfo(aid,email,gender,city,birthday,filename) and ahelper.updateNickNameByAid(aid,nickName):
            re = make_response("OK")
        else:
            re = make_response("Failed")
        return re
    elif keyword == "password":
        new_pwd = request.form['register_pwd']
        if ahelper.updatePasswordByAid(aid,new_pwd):
            re = make_response("OK")
        else:
            re = make_response("Error")
        return re
@app.route('/<aid>/admin',methods=['GET','POST'])
def admin_page(aid):
    '''direct to admin page'''

    if 'admin_model' not in session or aid != session['admin_model']:
        abort(404);
    try:
        keyword = request.args.get('page')
        if keyword == 'viewpost':
            return render_template("admin_view_post.html")
    except KeyError:
        pass
    return render_template("admin.html")
@app.route('/<aid>/admin/delete/author',methods=['GET'])
def admin_author_delete(aid):
    '''delete author in admin'''

    if 'admin_model' not in session or aid != session['admin_model']:
        abort(404);
    try:
        keyword = request.args.get('aid')
        if ahelper.deleteAuthor(keyword) == True:
            re = make_response("OK")
        else:
            re = make_response("Wrong")
        return re
    except KeyError:
        return "Wrong URL",404
@app.route('/<aid>/admin/delete/post',methods=['GET'])
def admin_post_delete(aid):
    '''delete post in admin'''

    if 'admin_model' not in session or aid != session['admin_model']:
        abort(404);
    try:
        keyword = request.args.get('pid')
        if postHelper.deletePostByPid(keyword) == True:
            re = make_response("OK")
        else:
            re = make_response("Wrong")
        return re
    except KeyError:
        return "Wrong URL",404
@app.route('/<aid>/admin/author/approve',methods=['GET'])
def admin_author_approve(aid):
    '''approve application in admin'''

    if 'admin_model' not in session or aid != session['admin_model']:
        abort(404);
    try:
        keyword = request.args.get('aid')
        if ahelper.confirmAuthor(keyword) == True:
            re = make_response("OK")
        else:
            re = make_response("Wrong")
        return re
    except KeyError:
        return "Wrong URL",404
@app.route('/<aid>/admin/author/deny',methods=['GET'])
def admin_author_deny(aid):
    '''deny application in admin'''

    if 'admin_model' not in session or aid != session['admin_model']:
        abort(404);
    try:
        keyword = request.args.get('aid')
        if ahelper.deleteAuthor(keyword) == True:
            re = make_response("OK")
        else:
            re = make_response("Wrong")
        return re
    except KeyError:
        return "Wrong URL",404
@app.route('/<aid>/admin/view/post',methods=['GET'])
def admin_get_post(aid):
    '''get post in admin mode'''

    if 'admin_model' not in session or aid != session['admin_model']:
        abort(404);
    try:
        keyword = request.args.get('aid')
        post = postController.getPostByAid(keyword)
        return post,200
    except KeyError:
        return "Wrong URL",404
@app.route('/<aid>/admin/view/circle',methods=['GET'])
def admin_get_circle(aid):
    '''get friendship in admin mode'''

    if 'admin_model' not in session or aid != session['admin_model']:
        abort(404);
    try:
        keyword = request.args.get('aid')
        re = circleController.getFriendList(keyword)
        return re
    except KeyError:
        return "Wrong URL",404
@app.route('/<aid>/admin/view/tmp_author',methods=['GET'])
def admin_get_tmp_author(aid):
    '''get the author that haven't been approve by admin'''

    if 'admin_model' not in session or aid != session['admin_model']:
        abort(404);
    response = aController.getAllTmpAuthor();
    if response == None:
        response = make_response("ERROR")
    return response
@app.route('/<aid>/admin/manage/<otheraid>',methods=['POST'])
def admin_change_author(aid,otheraid):
    '''update the author profile in admin'''

    if 'admin_model' not in session or aid != session['admin_model']:
        abort(404);
    return change_author_profile(otheraid)
@app.route('/<aid>/admin/global_setting/signup_policy',methods=['GET'])
def admin_change_signup_policy(aid):
    '''adjust the forum is open register or not in admin mode'''

    if 'admin_model' not in session or aid != session['admin_model']:
        abort(404)
    try:
        operation = request.args.get('operation')
        if operation == 'turunon':
            settingHelper.removeSignUpRestriction()
            re = make_response("OK")
        elif operation == 'turnoff':
            settingHelper.addSignUpRestriction()
            re = make_response("OK")
        else:
            re = make_response("Error",404)
        return re
    except KeyError:
        return "Wrong URL",404
@app.route('/ajax/aid')
def getuid():
    '''get the user id'''

    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        re = make_response(session['logged_id'])
        re.headers['Content-Type']='text/plain'
        return re
@app.route('/ajax/author_name')
def getaname():
    '''get the username'''

    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        re = make_response(session['logged_in'])
        re.headers['Content-Type']='text/plain'
        return re

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''author login'''

    if request.method == 'POST':
        authorName =request.form['username']
        password =request.form['password']
        json_str = ahelper.authorAuthenticate(authorName,password)
        print json_str
        if  json_str == False:
            re = make_response("False")
            re.headers['Content-Type']='text/plain'
            return re ,200
        elif json_str=="NO_CONFIRMED":
            re = make_response("NO_CONFIRMED")
            return re ,200
        else:
            session['logged_in'] = authorName
            session['logged_id'] = json.loads(json_str)['aid']
            if(session['logged_id']==admin_id):
                session['admin_model']= admin_id;
            return json_str,200
    else:
        if not session.get('oauth_state'):
            session['oauth_state'] = binascii.hexlify(os.urandom(24))
            authorize_url = github.get_authorize_url(scope='user,notifications', state=session.get('oauth_state'))
            return render_template('header.html',authorize_url=authorize_url)
        else:
            return render_template('header.html',github=True)

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
    '''new user register'''

    if request.method == 'POST':
        #parse require information
        gender=""
        email = request.form['email']
        authorName=request.form['author_name']
        password=request.form['register_pwd']
        #parse optional information
        file = request.files['profile_image']
        #print "--"+file.filename
        nickName=request.form['nick_name']
        birthday =request.form['birthday']
        city = request.form['city']
        try:
            gender = request.form['gender']
        except KeyError:
            gender = ""
        if REGISTER_RESTRICTION:
            aid_json = ahelper.addLocalTmpAuthor(authorName,password,nickName)
        else:
            aid_json = ahelper.addAuthor(authorName,password,nickName)
        if aid_json == False:
            re = make_response("False")
            re.headers['Content-Type']='text/plain'
            return re
        else:
            aid = json.loads(aid_json)['aid']
            if not REGISTER_RESTRICTION:
                session['logged_in'] = authorName
                session['logged_id'] = aid
        path =""
        if(file!=None and file.filename!=""):
            path = save_image(aid,file)
        if ahelper.updateAuthorInfo(aid,email,gender,city,birthday,path) ==False:
            abort(500)
        if not REGISTER_RESTRICTION:
            return aid_json
        else:
            re= make_response("NO_CONFIRMED")
            return re
    return redirect(url_for('/'))

def save_image(aid,file):
    '''upload the new image into service'''

    filename = aid+"."+file.filename.rsplit('.', 1)[1]
    path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    file.save(path)
    return filename
@app.route('/<aid>/recommended_authorlist.json', methods=['GET'])
def authorlist(aid):
    '''redirect to all author list'''

    if ('logged_in' not in session) or (aid !=session['logged_id']):
        return redirect(url_for('/'))
    re = aController.getRecommendedAuthor(aid)
    return re

# search authors with keyword
@app.route('/<aid>/author/search',methods=['GET'])
def search_author(aid):
    '''search author by aid'''  

    if ('logged_in' not in session) or (aid !=session['logged_id']):
        return redirect(url_for('/'))
    try:
        keyword = request.args.get('key')
    except KeyError:
        return redirect(url_for('/'))
    if keyword!=None and keyword!="":
        re = aController.searchAuthorByString(aid,keyword)
        return re

@app.route('/<aid>/authorlist.json',methods=['GET'])
def allauthorlist(aid):
    '''get all author by aid'''

    if ('logged_in' not in session) or (aid !=session['logged_id']):
        return redirect(url_for('/'))
    re = aController.getOtherAuthor(aid)
    #print re
    return re

@app.route('/<aid>/circlelist.json',methods=['GET'])
def circleauthorlist(aid):
    '''get the friendship list by author id'''  

    if ('logged_in' not in session) or (aid !=session['logged_id']):
        return redirect(url_for('/'))
    re = circleController.getFriendList(aid)
    #print re
    return re

@app.route('/<aid>/circle',methods=['GET'])
def render_circle_modal(aid):
    '''render the friendship modal by aid'''

    if ('logged_in' not in session) or (aid !=session['logged_id']):
        return redirect(url_for('/'))
    return render_template('view_circles_modal.html')

@app.route('/<aid>/circle/delete',methods=['GET'])
def delete_friends(aid):
    '''delete firends by aid'''

    if ('logged_in' not in session) or (aid !=session['logged_id']):
        return redirect(url_for('/'))
    try:
        keyword = request.args.get('aid')
        if circleController.deleteFriendOfAuthor(aid,keyword):
            re =make_response("OK")
        else:
            re =make_response("Failed")
        return re
    except KeyError:
        return redirect(url_for('/'))

@app.route('/<aid>/messages.json', methods=['GET'])
def messages(aid):
    '''get all message by aid'''

    if ('logged_in' not in session) or (aid !=session['logged_id']):
        abort(404)
    else:
        jsonstring = reController.getAllRequestByAid(aid)
        return jsonstring

# logout
@app.route('/logout')
def logout():
    '''logout'''
    session.pop('logged_in', None)
    session.pop('oauth_state', None)
    return redirect(url_for('login'))
    
# make request
@app.route('/<aid>/author/request',methods=['GET'])
def addfriend(aid):
    '''send add friend request'''

    if ('logged_in' not in session) or (session['logged_id'] != aid):
        abort(404)
    else:
        try:
            request_aid = request.args.get('recipient')
            if reController.sendRequest(aid,request_aid) is True:
                re = make_response("OK",200)
                return re
            else:
                re = make_response("Existed",409)
                return re
        except KeyError:
            return redirect(url_for(aid))
#accept request
@app.route('/<recipientAid>/author/request/accept',methods=['GET'])
def acceptRequest(recipientAid):
    if ('logged_in' not in session) or (session['logged_id'] != recipientAid):
        return redirect(url_for('/'))
    else:
        try:
            senderAid = request.args.get('sender')

            if( not aController.isRemoteAuthor(senderAid) ):

                if( reController.acceptRequestFromSender(recipientAid,senderAid) ):
                    re = make_response("OK",200)
                else:
                    re = make_response("Failed")
                return re
            else:
                remoteAuthor = aController.getAuthorInfoByAid(senderAid)
                localAuthor = aController.getAuthorInfoByAid(recipientAid)
                print("+++"+remoteAuthor.getAid())
                print("+++"+localAuthor.getAid())
                recipientAid = localAuthor.getAid()
                recipientName = localAuthor.getNickname()
                remoteSenderAid = remoteAuthor.getAid()
                remoteUrl = serverController.getServerUrlBySid(remoteAuthor.getSid())

                response = sendAcceptRequestToRemoteServer(recipientAid,recipientName,remoteSenderAid,remoteUrl)

                if(response == True):
                    re = make_response("OK",200)
                else:
                    re = make_response("Failed")
                return re

        except KeyError:
            return redirect(url_for('aid'))
#accept request

@app.route('/<aid>/author/request/deny',methods=['GET'])
def denyRequest(aid):
    '''deny friend request by author id'''   

    if ('logged_in' not in session) or (session['logged_id'] != aid):
        return redirect(url_for('/'))
    else:
        try:
            senderAid = request.args.get('sender')
            if reController.deleteRequest(senderAid,aid):
                re = make_response("OK")
                return re
            else:
                re = make_response("Fail")
                return re
        except KeyError:
            return redirect(url_for('aid'))

'''redirect to main html (posts)'''
@app.route('/author/<authorName>')
def renderStruct(authorName):
    if ('logged_in' in session) and (session['logged_in'] == authorName):
        return render_template('struct.html')
    else:
        return abort(404)

# get all the new posts that a specific author can view from the server
'''get post by author id'''
@app.route('/<aid>/pull/')
def getPostForAuthor(aid):


    if ('logged_in' in session) and (session['logged_id'] == aid):
        #aid = session['logged_id']
        if aid == None:
            return json.dumps({'status':None}),200
        else:
            post = postController.getPost(aid)
            return post,200
    else:
        return abort(404)

'''main function of send markdown'''
@app.route('/markdown',methods=['GET','POST'])
def index():

    if request.method == 'POST':
        content = request.form['postContent']
        content = Markup(markdown.markdown(content))
        html_string =  render_template('markdown.html', **locals())
        print html_string
        return html_string
    return render_template('markdown_input.html')


'''get comments by author'''
@app.route('/author/<aid>/posts/comments/',methods=['GET'])
def getCommentsForAuthor(aid):

    if ('logged_in' in session) and (session['logged_id'] == aid):
        return commentController.getCommentsForAuthor(aid),200
    else:
        return abort(404)

'''check whether the file user upload is allowed or not'''
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.' ,1)[1] in app.config['ALLOWED_EXTENSIONS']


'''upload new image by author id and post id'''
@app.route('/<aid>/<pid>/upload',methods=['POST'])
def upload(aid,pid):

    if ('logged_in' not in session) or (session['logged_id'] != aid):
        abort(404)
    file = request.files['img_file']
    if file:
        if not allowed_file(file.filename):
            re = make_response("Wrong Type");
        else:
            filename = save_image(pid,file)
            iid =  imageHelper.insertImage(filename,aid,pid)
            if iid !=False:
                re = make_response("OK");
            else:
                re = make_response("DatabaseError")
        return re
    else:
        abort(404)

'''view the image in post by author id'''
@app.route('/<aid>/<pid>/image/view',methods=['GET'])
def viewPostImage(aid,pid):

    if ('logged_in' not in session) or (session['logged_id'] != aid):
        abort(404)
    image = imageHelper.getImageByPid(pid)
    if image == False:
        re = make_response("DatabaseError")
        return re
    else:
        if len(image) >0:
            filename = image[0].getPath();
            return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
        else:
            return send_from_directory(app.config['UPLOAD_FOLDER'],"unfound.gif")


'''upload new post to server by author name'''
@app.route('/<authorName>/post',methods=['PUT','POST'])
def uploadPostToServer(authorName):

    if ('logged_in' in session) and (session['logged_in'] == authorName):
        aid = session['logged_id']
        postName = authorName
        postObj = flaskPostToJson()
        try:
            type = request.args.get('markdown')
            postMsg = postObj['message']
            if type =='true':
                content = Markup(markdown.markdown(postMsg))
                postMsg = render_template('markdown.html', **locals())
        except KeyError:
            return "Wrong URL",404
        postTitle = postObj['title']
        postType = postObj['type']
        postPermission = postObj['permission']
        postDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        if aid == None:
            return json.dumps({'status':False}),200
        else:
            newPost = Post(None,aid,postName,postDate,postTitle,postMsg,postType,postPermission)
            result = postHelper.addPost(aid,postTitle,postMsg,postType,postPermission)
        return json.dumps({'status':result}),200
    else:
        return abort(404)

'''Retrive the posting permission information for a specific author by authorName'''
@app.route('/<authorName>/post/getPermissionList/',methods=['GET'])
def getPermissionList(authorName):

    if ('logged_in' in session) and (session['logged_in'] == authorName):
        if request.method == 'GET':
            aid = session['logged_id']
            # Get the permission: friend or fof, from parameter 
            permission = request.args.get('option')

            if permission == "specify":
                friendlist = circleHelper.getFriendList(aid)	
                if friendlist != None:
                    return json.dumps(friendlist),200
    else:
        return abort(404)

'''Get all the comments for a specific post from DB'''
@app.route('/author/<aid>/posts/<pid>/comments/',methods=['GET'])
def getCommentsForPost(aid,pid):
    

    if('logged_id' in session) and (session['logged_id'] == aid):
        result = commentController.getCommentsForPost(pid)
        return result,200
    else:
        return abort(404)

'''Add a comment for a specific post into DB'''
@app.route('/author/<aid>/posts/<pid>/comments/',methods=['PUT','POST'])
def addCommentForPost(aid,pid):    

    if ('logged_in' in session) and (session['logged_id'] == aid):
        
        commentObj = flaskPostToJson()
        
        #Follow the json example on github
        aid = commentObj['posts'][0]['author']['id']
        content = commentObj['posts'][0]['comments'][0]['comment']
        pid = commentObj['posts'][0]['guid']

        result = commentController.addCommentForPost(aid,pid,content)
        if result != None:
            return result,200
        else:
            return None,200
    else:
        return abort(404)


'''get the notification by author'''
# get all the new posts that a specific author can view from the server
@app.route('/<authorName>/github/notification')
def getNotification(authorName):
    authorToken = authorName + '_authToken'
    if ('logged_in' in session) and (session['logged_in'] == authorName) and (authorToken in session):
        # get author auth token
        authorAuthToken=session[authorToken]
        # get auth session
        auth_session = github.get_session(token=authorAuthToken)
        aid = session['logged_id']
        if aid == None:
            return json.dumps({'status':None}),200
        else:
            author_notification = aid+'_notitfication'
            notification_number = session[author_notification]
            notifications={}
            r = auth_session.get('/users/'+authorName+'/received_events')

            #print r.json()
            for i in range(notification_number,len(r.json())):
                notification={}
                content=""
                title = ""
                repo=""
                ref=""
                for key,value in r.json()[i].iteritems():
                    if key == "payload":
                        for key1,value1 in value.iteritems():
                            if key1 == "commits":
                                for j in range(0,len(value1)):
                                    for key2,value2 in value1[j].iteritems():
                                        if key2 == "message":
                                            content = content + value2 + " "
                            elif key1 == "ref":
                                ref = value1
                    elif key == "created_at":
                        notification['time']=value
                    elif key == "actor":
                        for key1,value1 in value.iteritems():
                            if key1 == "login":
                                title = title + value1
                    elif key == "repo":
                        for key1,value1 in value.iteritems():
                            if key1 == "name":
                                repo = value1
                    elif key == "type":
                        if value == "PushEvent":
                            title = title + ' Push ' + repo + ' ' + ref
                        elif value == "CommitCommentEvent":
                            title = title + ' Commit Comment ' + repo + ' ' + ref
                        elif value == "CreateEvent":
                            title = title + ' Create ' + repo + ' ' + ref
                        elif value == "DeleteEvent":
                            title = title + ' Delete ' + repo + ' ' + ref
                        elif value == "DeploymentEvent":
                            title = title + ' Deploytment ' + repo + ' ' + ref
                        elif value == "DownloadEvent":
                            title = title + ' Download ' + repo + ' ' + ref
                        elif value == "FollowEvent":
                            title = title + ' Follow ' + repo + ' ' + ref
                        elif value == "ForkEvent":
                            title = title + ' Fork ' + repo + ' ' + ref
                notification['title']=title
                notification['content']=content
                notifications[i]=notification
            session[author_notification] = len(r.json())
        return json.dumps(notifications),200
    else:
        return abort(404)


'''get authorization from github'''
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
    aid = session['logged_id']
    author_notification = aid+'_notitfication'
    session[author_notification] = 0
    return redirect(url_for('login'))



'''get all the new posts that a specific author can view from the server '''
@app.route('/<aid>/pull/mypost')
def getMyPostForAuthor(aid):
    

    if ('logged_in' in session) and (session['logged_id'] == aid):
        #aid = session['logged_id']
        if aid == None:
            return json.dumps({'status':None}),200
        else:
            post = postController.getMyPost(aid)
            return post,200
    else:
        return abort(404)

'''get all posts by author'''
@app.route('/<authorName>/mypost')
def myPost(authorName):
    
    if ('logged_in' in session) and (session['logged_in'] == authorName):
        return render_template('mypost.html')
    else:
        abort(404);

'''delete my post by author'''
@app.route('/<authorName>/mypost/delete/<pid>')
def myPostDelete(authorName,pid):

    if ('logged_in' in session) and (session['logged_in'] == authorName):
        result = postHelper.deletePostByPid(pid)
	print result
        return render_template('mypost.html')
    else:
        abort(404);

'''
Public API: receieve the friend request from a remote server
'''
@app.route('/friendrequest',methods=['GET','POST'])
def friendRequestService():

    if(request.method == 'POST'):
        print(request)
        response = make_response()
        result = serviceController.receiveFriendRequestFromRemoteServer(json.loads(request.data))
        if(result):
            return make_response("", 200)
        else:
            return make_response("", 409)
    else:
        return make_response("", 409)

'''
Don't access this API from client side
This is for internal server to use only
'''
#@app.route('/response/accept')
def sendAcceptRequestToRemoteServer(recipientAid,recipientName,remoteSenderAid,remoteSid):
    
    payload = serviceController.sendFriendRequestToRemoteServer(recipientAid,recipientName,remoteSenderAid,remoteSid)
    if(payload != None):
        url = payload['friend']['host']
        headers = {'content-type': 'application/json'}
        print(payload)
        response = requests.post(url,data = json.dumps(payload),headers = headers )
        if(resposen.status == '200'):
            return True
        else:
            return False
    return False
'''
Public API: all posts marked as public on the server
'''
@app.route('/posts',methods=['GET'])
def sendPublicPostsToRemoteServer():
    
    payload = serviceController.sendPublicPostsToRemoteServer()
    if(payload != None):
        return json.dumps(payload),200
    else:
        return json.dumps([]),200
'''
Public API: send glabal authors to remote servers
'''
@app.route('/global/authors',methods=['GET'])
def sendGlobalAuthorsToRemoteServer():

    payload = serviceController.sendGlobalAuthorsToRemoteServer()
    if(payload != None):
        return json.dumps(payload),200
    else:
        return json.dumps([]),200

'''view images that have permission'''
@app.route('/permission/image/<imagename>',methods=['GET'])
def view_permission_image(imagename):

    imagename=PERMISSION_IMAGE+'/'+imagename+'.png'
    return send_file(imagename, mimetype='image/png')

'''upload post's permission by author'''
@app.route('/<authorName>/postpermission/<pid>',methods=['PUT','POST'])
def uploadPostPermissionToServer(authorName,pid):

    if ('logged_in' in session) and (session['logged_in'] == authorName):
        send = flaskPostToJson()
        checked = send['data']
        result = postPermissionHelper.addPostPermission(pid,checked)
        return json.dumps({'status':result}),200
    else:
        return abort(404)
        
if __name__ == '__main__':

    app.debug = True
    REGISTER_RESTRICTION = settingHelper.getSignUpRestrictionValue()
    POST_REMOTE_ACCESS_RESTRICTION = settingHelper.getRemotePostAccessRestrictionValue()
    IMAGE_REMOTE_ACCESS_RESTRICTION = settingHelper.getRemoteImageAccessRestrictionValue()
    app.run(host='0.0.0.0',port=8080)
