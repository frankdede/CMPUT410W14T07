import json
import flask
import markdown
from time import gmtime, strftime
from flask import Flask, request, redirect, url_for, g, render_template, flash, session, abort,make_response, Markup, send_from_directory,send_file
from werkzeug.utils import secure_filename
from random import randrange
import sys,os
sys.path.append('sys/controller')
sys.path.append('sys/model')
from AuthorHelper import *
from DatabaseAdapter import *
from PostHelper import *
from RequestHelper import *
from CircleHelper import *
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
postcontroller = PostController(dbAdapter)
#
reController = RequestController(dbAdapter)
#
circleHelper = CircleHelper(dbAdapter)
circleController = CircleController(dbAdapter)
#
commentController = CommentController(dbAdapter)
#Allowed file extensions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config.from_object(__name__)
# add upload
UPLOAD_FOLDER='upload/image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    print imagename
    return send_from_directory(app.config['UPLOAD_FOLDER'],imagename, as_attachment=False)
@app.route('/<aid>/profile.json',methods=['GET'])
def get_profile(aid):
    try:
        re_aid = request.args.get("aid")
        re = aController.getAuthorByAid(re_aid)
        print re
        if re != False:
            return re
        return redirect(url_for('/'))
    except KeyError:
        return redirect(url_for('/'))

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
        print "--"+file.filename
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
            path =""
            if(file!=None or file.name!=""):
                path = save_image(aid,file)
            if ahelper.updateAuthorInfo(aid,email,gender,city,birthday,path) ==False:
                abort(500)
            return aid_json
    return redirect(url_for('/'))

def save_image(aid,file):
    filename = aid+"."+file.filename.rsplit('.', 1)[1]
    path = os.path.join(app.config['UPLOAD_FOLDER'])
    file.save(path, filename)
    return path
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
    print re
    return re
@app.route('/<aid>/circlelist.json',methods=['GET'])
def circleauthorlist(aid):
    if ('logged_in' not in session) or (aid !=session['logged_id']):
        return redirect(url_for('/'))
    re = circleController.getFriendList(aid)
    print re
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
        print jsonstring
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

    if ('logged_in' in session) and (session['logged_in'] == aid):
        aid = session['logged_id']
        if aid == None:
            return json.dumps({'status':None}),200
        else:    
            post = postcontroller.getPost(aid)
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

@app.route('/author/<aid>/post/<pid>/comments',methods=['GET'])
def getAllCommentsForPost(aid,pid):

    if ('logged_in' in session) and (session['logged_in'] == aid):
        self.commentController.getAllCommentsForPost(pid)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.' ,1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/test')
def test():
    return render_template('upload_image.html')

@app.route('/upload',methods=['POST'])
def upload():
    file = request.files['file']
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
        #aid = ahelper.getAidByAuthorName(authorName)
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

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
