
from flask import Flask, request, redirect, url_for, g, render_template, flash, session, abort,make_response
import sys,os
sys.path.append('sys/controller')
from authorhelper import *
from databasehelper import *
DEBUG = True

dbhelper = Databasehelper()
ahelper = AuthorHelper()
dbhelper.connect()
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
@app.route('/author/<id>')
def renderStruct(id):
	return render_template('struct.html')


if __name__ == '__main__':
	app.debug = True
	app.run()
