
from flask import Flask, request, redirect, url_for, g, render_template, flash, session, abort,make_response
import sys,os
sys.path.append('sys/controller')
from authorhelper import *
from posthelper import *
from databasehelper import *
DEBUG = True
# create a new database obj
dbhelper = Databasehelper()
# connect
dbhelper.connect()

ahelper = AuthorHelper()
# use the conneted dbHelper to initialize postHelper obj
postHelper = PostHelper(dbhelper)

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = os.urandom(24)
error = None

@app.route('/', methods=['GET', 'POST'])
def root():
	if 'logged_in' in session:
		return render_template('header.html')
	else:
		return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username =request.form['username']
		password =request.form['password']
		if ahelper.authorauthenticate(dbhelper,username,password):
			session['logged_in'] = username
			error="login successful"
			re = make_response("True")
			re.headers['Content-Type']='text/plain'
			return re
		else:
			re = make_response("False")
			re.headers['Content-Type']='text/plain'
			return re
	return render_template('header.html')
@app.route('/register', methods=['PUT', 'POST'])
def register():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        nick_name=request.form['nick_name']
        if ahelper.addauthor(dbhelper,username,password,nick_name):
            re = make_response("True")
            session['logged_in'] = username
            re.headers['Content-Type']='text/plain'
            return re
        else:
            re = make_response("False")
            re.headers['Content-Type']='text/plain'
            return re
	return redirect(url_for('/'))

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	return redirect(url_for('login'))

@app.route('/author/<autherName>')
def renderStruct(autherName):
	if 'logged_in' in session:
		return render_template('struct.html')
	else:
		return redirect('/templates/error/404.html');

# get all the new posts that a specific author can view from the server
@app.route('/pull/<id>')
def getUpdatedPosts(id):
	post = postHelper.getPostList(id);
 	return flask.jsonify(post),200

if __name__ == '__main__':
	app.debug = True
	app.run()
