
import json
import flask
from flask import Flask, request, redirect, url_for, g, render_template, flash, session, abort,make_response
from werkzeug.utils import secure_filename

import sys,os
sys.path.append('sys/controller')
sys.path.append('sys/model')
from authorhelper import *
from posthelper import *
from databasehelper import *
#from requesthelper import *
from circlehelper import *
#allowed file extension
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
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
# add upload
UPLOAD_FOLDER='/upload/image'
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
    #username = session['logged_in']
    #mumMsg = reHelper.getMessageCountByAuthorName(username)
    
    return render_template('header.html')
@app.route('/addfriend', methods=['GET', 'POST'])
def addfriend():
        #username = session['logged_in']
        #mumMsg = reHelper.getMessageCountByAuthorName(username)
    
    return render_template('addfriend.html')
@app.route('/authorlist.json', methods=['GET'])
def authorlist():
    #test data
    tem =['Mark','Hello','Frank']
    jsonstring= json.dumps(tem)
    return jsonstring
@app.route('/<aid>/request/<aname>',methods=['post'])
def make_request(aid,aname):
    re = make_response("ok")
    re.headers['Content-Type']='test/plain'
    return re
@app.route('/admin/authormanage/author_list.json',methods=['GET'])
def get_all_author_list():
    tem =['Mark','Hello','Frank']
    jsonstring= json.dumps(tem)
    return jsonstring
@app.route('/admin/authormanage/delete/<aid>',methods=['GET'])
def delete_author():
    return jsonstring
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
@app.route('/<aid>/uploadprofile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    pass
if __name__ == '__main__':
    app.debug = True
    app.run()
