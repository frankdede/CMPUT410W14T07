import json
import flask
import markdown
from time import gmtime, strftime
from flask import Flask, request, redirect, url_for, g, render_template, flash, session, abort,make_response, Markup, send_from_directory,send_file
from werkzeug.utils import secure_filename
from random import randrange
import sys,os
from mimetypes import MimeTypes
import urllib
import binascii
from rauth import OAuth2Service
sys.path.append('sys/controller')
sys.path.append('sys/model')
from AuthorHelper import *
from DatabaseAdapter import *
from PostHelper import *
from RequestHelper import *
from CircleHelper import *
from SettingHelper import *
from PostController import *
from AuthorController import *
from RequestController import *
from CommentController import *

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
#Allowed file extensions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config.from_object(__name__)
REGISTER_RESTRICATION = None
# add upload
UPLOAD_FOLDER='upload/image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)
admin_id = '000000'
admin_name='admin'
admin_model = False
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
    if 'logged_in' in session and aid ==session['logged_id']:
        username = session['logged_in']
        msgCount = reController.getRequestCountByAid(aid)
        countnumber = json.loads(msgCount)['count']
        return render_template('header.html',msgCount = countnumber)
    else:
        return redirect(url_for('login'))

@app.route('/<aid>/profile',methods=['GET'])
def view_profile(aid):
    return render_template('profile.html')

@app.route('/<aid>/profile/image/<imagename>',methods=['GET'])
def view_profile_image(aid,imagename):
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
    if 'logged_in' in session and aid ==session['logged_id']:
        try:
            re_aid = request.args.get("aid")
            re = aController.getAuthorByAid(re_aid)
            #print re
            if re != False:
                return re
            return redirect(url_for('/'))
        except KeyError:
            return redirect(url_for('/'))
    return redirect(url_for('/'))
    
@app.route('/<aid>/profile/change',methods=['POST'])
def change_profile(aid):
    if 'logged_in' in session and aid ==session['logged_id']:
        return change_author_profile(aid)
    else:
        return redirect(url_for('/'))
def change_author_profile(aid):
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
@app.route('/<aid>/admin/author/approve',methods=['GET'])
def admin_author_approve(aid):
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
    if 'admin_model' not in session or aid != session['admin_model']:
        abort(404);
    response = aController.getAllTmpAuthor();
    if response == None:
        response = make_response("ERROR")
    return response
@app.route('/<aid>/admin/manage/<otheraid>',methods=['POST'])
def admin_change_author(aid,otheraid):
    if 'admin_model' not in session or aid != session['admin_model']:
        abort(404);
    return change_author_profile(otheraid)
@app.route('/<aid>/admin/global_setting/signup_policy',methods=['GET'])
def admin_change_signup_policy(aid):
    if 'admin_model' not in session or aid != session['admin_model']:
        abort(404)
    try:
        operation = request.args.get('operation')
        if operation == 'turunon':
            settingHelper.removeSignUpRestrication()
            re = make_response("OK")
        elif operation == 'turnoff':
            settingHelper.addSignUpRestrication()
            re = make_response("OK")
        else:
            re = make_response("Error",404)
        return re
    except KeyError:
        return "Wrong URL",404
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
        if REGISTER_RESTRICATION:
            aid_json = ahelper.addLocalTmpAuthor(authorName,password,nickName)
        else:
            aid_json = ahelper.addAuthor(authorName,password,nickName)
        if aid_json == False:
            re = make_response("False")
            re.headers['Content-Type']='text/plain'
            return re
        else:
            aid = json.loads(aid_json)['aid']
            if not REGISTER_RESTRICATION:
                session['logged_in'] = authorName
                session['logged_id'] = aid
        path =""
        if(file!=None and file.filename!=""):
            path = save_image(aid,file)
        if ahelper.updateAuthorInfo(aid,email,gender,city,birthday,path) ==False:
            abort(500)
        if not REGISTER_RESTRICATION:
            return aid_json
        else:
            re= make_response("NO_CONFIRMED")
            return re
    return redirect(url_for('/'))

def save_image(aid,file):
    filename = aid+"."+file.filename.rsplit('.', 1)[1]
    path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    file.save(path)
    return filename
@app.route('/image/view/<name>',methods=['GET'])
def view_imagin():
    pass
@app.route('/<aid>/recommended_authorlist.json', methods=['GET'])
def authorlist(aid):
    if ('logged_in' not in session) or (aid !=session['logged_id']):
        return redirect(url_for('/'))
    re = aController.getRecommendedAuthor(aid)
    return re

# search authors with keyword
@app.route('/<aid>/author/search',methods=['GET'])
def search_author(aid):
    if ('logged_in' not in session) or (aid !=session['logged_id']):
        return redirect(url_for('/'))
    try:
        keyword = request.args.get('key')
    except KeyError:
        return redirect(url_for('/'))
    if keyword!=None and keyword!="":
        re = aController.searchAuthorByString(keyword)
        return re

@app.route('/<aid>/authorlist.json',methods=['GET'])
def allauthorlist(aid):
    if ('logged_in' not in session) or (aid !=session['logged_id']):
        return redirect(url_for('/'))
    re = aController.getOtherAuthor(aid)
    #print re
    return re

@app.route('/<aid>/circlelist.json',methods=['GET'])
def circleauthorlist(aid):
    if ('logged_in' not in session) or (aid !=session['logged_id']):
        return redirect(url_for('/'))
    re = circleController.getFriendList(aid)
    #print re
    return re

@app.route('/<aid>/circle',methods=['GET'])
def render_circle_modal(aid):
    if ('logged_in' not in session) or (aid !=session['logged_id']):
        return redirect(url_for('/'))
    return render_template('view_circles_modal.html')

@app.route('/<aid>/circle/delete',methods=['GET'])
def delete_friends(aid):
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
    if ('logged_in' not in session) or (aid !=session['logged_id']):
        abort(404)
    else:
        jsonstring = reController.getAllRequestByAid(aid)
        #print jsonstring
        return jsonstring
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
#accept request
@app.route('/<aid>/author/request/accept',methods=['GET'])
def accept_request(aid):
    if ('logged_in' not in session) or (session['logged_id'] != aid):
        return redirect(url_for('/'))
    else:
        try:
            accept_aid = request.args.get('sender')
            if reController.acceptRequestFromSender(aid,accept_aid):
                re = make_response("OK")
            else:
                re = make_response("Fail")
            return re
        except KeyError:
            return redirect(url_for('aid'))
#accept request
@app.route('/<aid>/author/request/deny',methods=['GET'])
def deny_request(aid):
    if ('logged_in' not in session) or (session['logged_id'] != aid):
        return redirect(url_for('/'))
    else:
        try:
            deny_aid = request.args.get('sender')
            if reController.deleteRequest(accept_aid,aid):
                re = make_response("OK")
            else:
                re = make_response("Fail")
        except KeyError:
            return redirect(url_for('aid'))
@app.route('/author/<authorName>')
def renderStruct(authorName):

    if ('logged_in' in session) and (session['logged_in'] == authorName):
        return render_template('struct.html')
    else:
        return abort(404)

# get all the new posts that a specific author can view from the server
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

@app.route('/markdown',methods=['GET','POST'])

def index():
    if request.method == 'POST':
        content = request.form['postMarkDown']
        content = Markup(markdown.markdown(content))
        return render_template('markdown.html', **locals())
    return render_template('markdown_input.html')

@app.route('/author/<aid>/posts/comments/',methods=['GET'])
def getCommentsForAuthor(aid):

    if ('logged_in' in session) and (session['logged_id'] == aid):
        return commentController.getCommentsForAuthor(aid),200
    else:
        return abort(404)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.' ,1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/test')
def test():
    return render_template('upload_image.html')

@app.route('/upload',methods=['POST'])
def upload():
    file = request.files['img_file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        return redirect(url_for('uploadImage',filename=filename))

@app.route('/uploads/<filename>')
def uploadImage(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)



@app.route('/<authorName>/post/',methods=['PUT','POST'])
def uploadPostToServer(authorName):

    if ('logged_in' in session) and (session['logged_in'] == authorName):
        aid = session['logged_id']
        postName = authorName
        postObj = flaskPostToJson()
        postTitle = postObj['title']
        postMsg = postObj['message']
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
'''
Retrive the posting permission information for a specific author by authorName
'''
@app.route('/<authorName>/post/getPermissionList/',methods=['GET'])
def getPermissionList(authorName):

    if ('logged_in' in session) and (session['logged_in'] == authorName):
        if request.method == 'GET':
            aid = session['logged_id']
            # Get the permission: friend or fof, from parameter 
            permission = request.args.get('option')

            if permission == "friends":
                friendlist = circleHelper.getFriendList(aid)	
                if friendlist != None:
                    return json.dumps(friendlist),200

            elif permission == "fof":
                fof = circleHelper.getFriendOfFriendList(aid)

                if fof != None:
                    return json.dumps(fof),200
                else:
                    return "null",200
                    return "null",200
    else:
        return abort(404)

'''
Get all the comments for a specific post from DB
'''
@app.route('/author/<aid>/posts/<pid>/comments/',methods=['GET'])
def getCommentsForPost(aid,pid):

    if('logged_id' in session) and (session['logged_id'] == aid):
        result = commentController.getCommentsForPost(pid)
        return result,200
    else:
        return abort(404)
'''
Add a comment for a specific post into DB
'''
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
            r = auth_session.get('/notifications')
            for i in range(notification_number,len(r.json())):
                notification={}
                for key,value in r.json()[i].iteritems():
                    if key == "updated_at":
                        print "updatet time: " + value
                        notification['time']=value
                    elif key == "subject":
                        for key1,value1 in value.iteritems():
                            if key1 == "url":
                                print "update at: " + value1
                                notification['url']=value1
                            elif key1 == "title":
                                print "title :" + value1
                                notification['title']=value1
                notifications[i]=notification
            session[author_notification] = len(r.json())
        #r = auth_session.put('/notifications')
        return json.dumps(notifications),200
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
    aid = session['logged_id']
    author_notification = aid+'_notitfication'
    session[author_notification] = 0
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.debug = True
    REGISTER_RESTRICATION = settingHelper.getSignUpRestricationValue()
    app.run(host='0.0.0.0')
