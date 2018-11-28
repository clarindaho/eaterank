import configparser
from flask import Flask, render_template, request, session
import mysql.connector
from time import sleep


from zomato import *
from restaurant import restaurant

import queries

# Read configuration from file.
config = configparser.ConfigParser()
config.read('config.ini')

# Set up application server.
app = Flask(__name__)

# Create a function for fetching data from the database.
def sql_query(sql, params = None):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

def sql_execute(sql, params):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor()
    cursor.execute(sql, params)
    db.commit()
    cursor.close()
    db.close()

@app.route('/')

@app.route('/index')
def index():
	page = {'author': 'Seohyun'}

	return render_template('index.html', page=page)


# Group Leader:
@app.route('/group/create')
def create_group():
	page = {
		'author': 'Clarinda',
		'title': 'Eaterank: Create Group',
		'description': 'Create groups for voting on restaurants.'
	}

	sql_execute(INSERT_CREW)
	crew_id = sql_query(GET_LAST_INSERT_ID)

	return render_template('creategroup.html', page=page, crew_id = crew_id)

@app.route('/zipcode', methods=["GET", "POST"])
def set_zipcode():
	page = {'author': 'Jason'}
	if request.method == "GET":
		return redirect(url_for("index"))
	if request.method == "POST":
		form = request.form
		crew_id = ""
		if "crew_id" in form:
			crew_id = form["crew_id"]
		if "zipcode" in form:
			#session["zipcode"] = form["zipcode"]
			zipcode = form["zipcode"]
			cuisines = getCuisinesZip(zipcode)
			return render_template('selectcuisines.html', zipcode = zipcode, cuisines = cuisines, crew_id = crew_id, page=page)

@app.route('/waitingleader', methods=["GET", "POST"])
def waiting():
	page = {'author': 'hello'}
	if request.method == "GET":
		return redirect(url_for("index"))
	if request.method == "POST":
		form = request.form
		zipcode = ""
		crew_id = ""
		cuisines = []
		for key in form:
			if (key == "zipcode"):
				zipcode = form[key]
			if (key == "crew_id"):
				crew_id = form[key]
			else:
				c = (key, form[key])
				cuisines.append(c)
		restaurants = getRestaurants(cuisines, zipcode)
		# insert restaurants and associated votes into database
		for r in restaurants:
			restaurant_params = (r.name, r.cuisine, r.address, r.rating, r.price_range, r.menu_url)
			#Database stuff
			sql_execute(INSERT_RESTAURANT, restaurant_params)
			restaurant_id = sql_query(GET_LAST_INSERT_ID)
			vote_params = (crew_id, restaurant_id)
			sql_execute(INSERT_VOTE, vote_params)

		return render_template("waiting.html", page=page, crew_id=crew_id)

@app.route('/startvoting', methods=["GET", "POST"])
def start_voting():
	page = {'author': 'hello'}
	if request.method == "GET":
		return redirect(url_for("index"))
	if request.method == "POST":
		form = request.form
		crew_id = form["crew_id"]
		sql_execute(UPDATE_CREW_VOTING, (True, crew_id))
		restaurants = sql_query(GET_RESTAURANT_IDS, params=crew_id)
		restaurant = sql_query(GET_RESTID_INFO, restaurants[0])
		return render_template('voting.html', page = page, crew_id = crew_id, restaurant=restaurant, index=0, group_leader= True)

# Normal group members:
@app.route('/group/join')
def join_group():
	page = {
		'author': 'Seohyun',
		'title': 'Eaterank: Join Existing Group',
		'description': 'Join existing groups for voting on restaurants.'
	}

	return render_template('joingroup.html', page=page)

@app.route('/voting', methods = ["GET", "POST"])
def wait_user():
	page = {'author': 'hello'}
	if request.method == "GET":
		return redirect(url_for("index"))
	if request.method == "POST":
		form = request.form
		crew_id = form["crew_id"]
		result = sql_query(GET_CREW, params=crew_id)
		message = ""
        # invalid crew id
		if result == []:
			message = "You have entered an invalid crew id."
			return render_template('joingroup.html', message = message, page = page)
		else:
			result = sql_query(GET_CREW_VOTING, params=crew_id)
			vote_started = result[0]
            # voting has already started for the group - inform user
			if vote_started:
				message = "Voting has already started. Sorry."
				return render_template('joingroup.html', message = message, page = page)
            # wait for group leader to begin the voting process for entire group
			else:
				while True:
					result = sql_query(GET_CREW_VOTING, params=crew_id)
					vote_started = result[0]
					if vote_started:
						restaurants = sql_query(GET_RESTAURANT_IDS, params=crew_id)
						restaurant = sql_query(GET_RESTID_INFO, params=restaurants[0])
						return render_template('voting.html', page = page, crew_id = crew_id, restaurant=restaurant, index=0, group_leader= False)
					sleep(5)

@app.route('/votefor', methods = ["GET", "POST"])
def vote_for():
	page = {'author': 'hello'}
	if request.method == "GET":
		return redirect(url_for("index"))
	if request.method == "POST":
		form = request.form
		crew_id = form["crew_id"]
		restaurant_id = form["restaurant_id"]
		vote_num = sql_query(GET_VOTE_NUM, params=(crew_id, restaurant_id))[0]
		sql_execute(UPDATE_VOTE_COUNT, (vote_num + 1, crew_id, restaurant_id))
		index = form["index"] + 1
		restaurants = sql_query(GET_RESTAURANT_IDS, params=crew_id)
		group_leader = form["group_leader"]
		if index < len(restaurants) - 1:
			restaurant = sql_query(GET_RESTID_INFO, params=restaurants[index])
			return render_template('voting.html', page = page, crew_id = crew_id, restaurant=restaurant, index=index, group_leader=group_leader)
		else:
			if group_leader:
				return render_template('end_voting.html', page = page, crew_id = crew_id)
			# regular user has to wait for the group leader to request final result
			else:
				while True:
					selected_restaurantID = sql_query(GET_CREW_SELECTED_REST, params=crew_id)[0]
					if selected_restaurantID != None:
						restaurant = sql_query(GET_RESTID_INFO, params=selected_restaurantID)[0]
						return render_template('results.html', page = page, crew_id = crew_id, restaurant = restaurant)
					sleep(5)

# user votes against restaurant - proceed to next restaurant or wait for results to appear
@app.route('/voteagainst', methods = ["GET", "POST"])
def vote_against():
	page = {'author': 'hello'}
	if request.method == "GET":
		return redirect(url_for("index"))
	if request.method == "POST":
		form = request.form
		crew_id = form["crew_id"]
		index = form["index"] + 1
		restaurants = sql_query(GET_RESTAURANT_IDS, params=crew_id)
		group_leader = form["group_leader"]
		if index < len(restaurants) - 1:
			restaurant = sql_query(GET_RESTID_INFO, params=restaurants[index])
			return render_template('voting.html', page = page, crew_id = crew_id, restaurant=restaurant, index=index, group_leader=group_leader)
		else:
			if group_leader:
				# have a end voting button that will take you to the results page
				return render_template('end_voting.html', page = page, crew_id = crew_id)
			# regular user has to wait for the group leader to request final result
			else:
				while True:
					selected_restaurantID = sql_query(GET_CREW_SELECTED_REST, params=crew_id)[0]
					if selected_restaurantID != None:
						restaurant = sql_query(GET_RESTID_INFO, params=selected_restaurantID)[0]
						return render_template('results.html', page = page, crew_id = crew_id, restaurant = restaurant)
					sleep(5)

# finds the selected restaurant after the group leader requests results
@app.route('/endvoting', methods = ["GET", "POST"])
def end_voting():
	page = {'author': 'hello'}
	if request.method == "GET":
		return redirect(url_for("index"))
	if request.method == "POST":
		form = request.form
		crew_id = form["crew_id"]
		selected_restaurantID = sql_query(SELECTED_RESTAURANT, params=crew_id)
		sql_execute(UPDATE_CREW_SELECTED_RESTAURANT, (selected_restaurantID, crew_id))
		restaurant = sql_query(GET_RESTID_INFO, params=selected_restaurantID)[0]
		return render_template('results.html', page = page, crew_id = crew_id, restaurant = restaurant)

if __name__ == '__main__':
	app.run(**config['app'])
