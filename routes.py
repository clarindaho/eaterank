from flask import render_template
from app import app

@app.route('/')

@app.route('/index')
def index():
	page = {'author': 'Seohyun'}
	
	return render_template('index.html', page=page)

@app.route('/group/create')
def create_group():
	page = 
	{
		'author': 'Clarinda',
		'title': 'Eaterank: Create Group',
		'description': 'Create groups for voting on restaurants.'
	}
	
	return render_template('creategroup.html', page=page)
	
@app.route('/group/join')
def join_group():
	page = 
	{
		'author': 'Seohyun',
		'title': 'Eaterank: Join Existing Group',
		'description': 'Join existing groups for voting on restaurants.'
	}

	return render_template('joingroup.html', page=page)