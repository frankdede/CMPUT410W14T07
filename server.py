import sqlite3
from flask import Flask, request, redirect, url_for, g, render_template, flash, session, abort
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
@app.route('/', methods=['GET', 'POST'])
def root():
	if 'logged_in' in session:
		return render_template('header.html', error=error)
	else:
		return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		username =request.form['username']
		password =request.form['password']
		if ahelper.authorauthenticate(dbhelper,username,password):
			session['logged_in'] = username
			error="login successful"
		else:
			error= "Username or Password Not Match"
	return render_template('header.html', error=error)
@app.route('/register', methods=['PUT', 'POST'])
def register():
	error = None
	username=request.form['username']
	password=request.form['password']
	nick_name=request.form['nick_name']
	if ahelper.addauthor(dbhelper,username,password,nick_name):
		return "add successfully"
	else:
		error = "Username Existed"
	return render_template('/login',error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.debug = True
	app.run()
