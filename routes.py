# Import libraries
from flask import Flask, redirect, render_template, request, session, url_for
from time import sleep

import re
import configparser
import mysql.connector
from queries import *

from zomato import *
from restaurant import restaurant

# Read configuration from file
config = configparser.ConfigParser()
config.read('config.ini')

# Set up application server
app = Flask(__name__)

# Create a function for fetching data from the database
def sql_query(sql, params = None):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

# Execute a SQL command
def sql_execute(sql, params):
	db = mysql.connector.connect(**config['mysql.connector'])
	cursor = db.cursor()
	cursor.execute(sql, params)
	db.commit()
	insert_id = cursor.lastrowid
	cursor.close()
	db.close()
	return insert_id
	
# Returns an array of cuisines without the ID
def get_cuisine_names(cuisines):
	cuisine_names = []
	
	for cuisine in cuisines:
		cuisine_name, cuisine_id = cuisine
		cuisine_names.append(cuisine_name)
		
	return cuisine_names

# Returns a cuisine tuple (cuisine_name, cuisine_id) for a specified cuisine_name
def get_cuisine_tuple(selected_cuisine_name, cuisines):
	for cuisine in cuisines:
		cuisine_name, cuisine_id = cuisine
		if selected_cuisine_name == cuisine_name:
			return cuisine

# Returns a cuisine_id for a specified cuisine_name
def get_cuisine_id(selected_cuisine_name, cuisines):
	for cuisine in cuisines:
		cuisine_name, cuisine_id = cuisine
		if selected_cuisine_name == cuisine_name:
			return cuisine_id


# Returns an array of selected cuisines		
def format_selected_cuisine(selected_cuisines):
	# Join all the characters in the array to a string
	formatted_selected_cuisines = ''.join(selected_cuisines)[1:-1]
	
	# Parse through the string to put together which cuisines were selected
	array_selected_cuisines = []
	selected_cuisine = None
	for char in formatted_selected_cuisines:
		if char is '\'':
			if selected_cuisine != None:
				# End of a selected cuisine
				array_selected_cuisines.append(selected_cuisine)
				selected_cuisine = None
			else:
				# Beginning of a selected cuisine
				selected_cuisine = ""
		elif char != ',' and selected_cuisine != None:
			# Build selected cuisine name
			selected_cuisine += char
	
	return array_selected_cuisines
	
"""
# Error page
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404
"""

# Home page
@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
	return render_template('index.html')

# Create group page
@app.route('/group/create', methods=["GET", "POST"])
def create_group():
	if request.method == "GET":
		return render_template('creategroup.html')
		
	if request.method == "POST":
		form = request.form
		
		# Get ZIP code
		zipcode = form["zipcode"]
		# check to see if a five-digit zipcode was submitted by the user
		pattern = r"(\b\d{5}\b)"
		zipcode = re.findall(pattern, zipcode)
		message = ""
		if zipcode == []:
			# not a valid zipcode
			message = "Invalid zipcode."
			return render_template('creategroup.html', message=message)
		else:
			# get the valid zipcode
			zipcode = zipcode[0]
			print("Zipcode" + str(zipcode))
			# Get cuisines based on the given ZIP code
			cuisines = getCuisinesZip(zipcode)
			if cuisines == []:
				# no cuisines are found
				message = "No cuisines found for that zipcode."
				return render_template('creategroup.html', message=message)
			cuisine_names = get_cuisine_names(cuisines)
		return render_template('creategroup.html', zipcode=zipcode, cuisines=cuisine_names)

@app.route('/group/create/<zipcode>', methods=["GET", "POST"])
def select_cuisine(zipcode):
	if request.method == "GET":
		# Get cuisines based on the given ZIP code
		cuisines = getCuisinesZip(zipcode)
		cuisine_names = get_cuisine_names(cuisines)
		
		return render_template('creategroup.html', zipcode=zipcode, cuisines=cuisine_names)
	
	if request.method == "POST":
		# Get cuisines based on the given ZIP code
		cuisines = getCuisinesZip(zipcode)
		cuisine_names = get_cuisine_names(cuisines)
	
		form = request.form
		
		# Get cuisines that were selected
		selected_cuisines = []
		for cuisine_name in cuisine_names:
			if form.get(cuisine_name) != None:
				selected_cuisines.append(cuisine_name)
		
		if len(selected_cuisines) == 0:
			return redirect(url_for("select_cuisine", zipcode=zipcode))
		else:
			# Create new crew in database and get its associated crew_id
			crew_id = sql_execute(INSERT_CREW, params=None)
			crew_id =int(crew_id)
			# Get cuisine_id for each of the selected cuisines
			cuisine_ids = []
			for selected_cuisine in selected_cuisines:
				cuisine_ids.append(get_cuisine_tuple(selected_cuisine, cuisines))
			
			# Get restaurants in the area (specified by ZIP code) associated with the specified cuisines (specified by ID)
			# Insert these restaurants and their associated votes (by the group) into the database
			restaurants = getRestaurants(cuisine_ids, zipcode)
			for r in restaurants:
				restaurant_params = (r.name, r.cuisine, r.address, r.rating, r.price_range, r.menu_url)
				print("CREW_ID: " + str(crew_id))
				# Database SQL execution
				restaurant_id = sql_query(RESTAURANT_EXISTS, params=(r.address,))[0][0]
				print("RESTAURANT_ID: " + str(restaurant_id))
				if restaurant_id == []:
					restaurant_id = sql_execute(INSERT_RESTAURANT, params=restaurant_params)[0]
					print("RESTAURANT_ID: " + str(restaurant_id))
				vote_params = (crew_id, restaurant_id)
				sql_execute(INSERT_VOTE, vote_params)
			
			return render_template('creategroup.html', zipcode=zipcode, cuisines=cuisine_names, selected_cuisines=selected_cuisines, crew_id=crew_id)

@app.route('/voting/waiting/<crew_id>', methods=["GET", "POST"])
def waiting(crew_id):
	start_voting_flag = 0

	if request.method == "GET":
		return redirect(url_for("index"))

	if request.method == "POST":
		return render_template("waiting.html", crew_id=crew_id, group_leader=1)

@app.route('/voting/waiting', methods=["GET", "POST"])			
def waiting_nongroupleader():
	if request.method == "GET":
		return redirect(url_for("index"))
	
	if request.method == "POST":
		form = request.form
		crew_id = form["group_code"]
		
		return render_template("waiting.html", crew_id=crew_id)

@app.route('/voting/start/<crew_id>/<group_leader>', methods=["GET", "POST"])
def start_voting(crew_id, group_leader):
	if request.method == "GET":
		return redirect(url_for("index"))
		
	if request.method == "POST":
		sql_execute(UPDATE_CREW_VOTING, (True, crew_id))
		restaurants = sql_query(GET_RESTAURANT_IDS, params=(crew_id,))
		restaurant = sql_query(GET_RESTID_INFO, restaurants[0])[0]
		restaurant_dict = {"restaurant_id": restaurant[0], "name": restaurant[1], "cuisine": restaurant[2], "address": restaurant[3], "rating": restaurant[4], "price_range": restaurant[5], "menu_url": restaurant[6]}
		return render_template('voting.html', crew_id = crew_id, restaurant=restaurant_dict, index=0, group_leader= True)

# Normal group members:
@app.route('/group/join')
def join_group():
	return render_template('joingroup.html')

@app.route('/voting', methods = ["GET", "POST"])
def wait_user():
	if request.method == "GET":
		return redirect(url_for("index"))
	if request.method == "POST":
		form = request.form
		crew_id = form["group_code"]
		result = sql_query(GET_CREW, params=(crew_id,))
		message = ""
        # invalid crew id
		if result == []:
			message = "You have entered an invalid crew id."
			return render_template('joingroup.html', message = message)
		else:
			result = sql_query(GET_CREW_VOTING, params=(crew_id,))
			vote_started = bool(result[0][0])
            # voting has already started for the group - inform user
			if vote_started:
				message = "Voting has already started. Sorry."
				return render_template('joingroup.html', message = message)
            # wait for group leader to begin the voting process for entire group
			else:
				while True:
					result = sql_query(GET_CREW_VOTING, params=(crew_id,))
					vote_started = bool(result[0][0])
					if vote_started:
						restaurants = sql_query(GET_RESTAURANT_IDS, params=(crew_id,))
						restaurant = sql_query(GET_RESTID_INFO, params=restaurants[0])[0]
						restaurant_dict = {"restaurant_id": restaurant[0], "name": restaurant[1], "cuisine": restaurant[2], "address": restaurant[3], "rating": restaurant[4], "price_range": restaurant[5], "menu_url": restaurant[6]}
						return render_template('voting.html', crew_id = crew_id, restaurant=restaurant_dict, index=0, group_leader= False)
					sleep(5)

@app.route('/votefor', methods = ["GET", "POST"])
def vote_for():
	page = {'author': 'hello'}
	if request.method == "GET":
		return redirect(url_for("index"))
	if request.method == "POST":
		form = request.form
		print(form)
		crew_id = int(form["crew_id"])
		restaurant_id = int(form["restaurant_id"])
		vote_num = sql_query(GET_VOTE_NUM, params=(crew_id, restaurant_id))[0][0]
		sql_execute(UPDATE_VOTE_COUNT, (vote_num + 1, crew_id, restaurant_id))
		index = int(form["index"]) + 1
		restaurants = sql_query(GET_RESTAURANT_IDS, params=(crew_id,))
		print("printing restaurants")
		print(restaurants)
		group_leader = form["group_leader"]
		if index < len(restaurants) - 1:
			restaurant = sql_query(GET_RESTID_INFO, params=restaurants[index])[0]
			restaurant_dict = {"restaurant_id": restaurant[0], "name": restaurant[1], "cuisine": restaurant[2], "address": restaurant[3], "rating": restaurant[4], "price_range": restaurant[5], "menu_url": restaurant[6]}
			return render_template('voting.html', page = page, crew_id = crew_id, restaurant=restaurant_dict, index=index, group_leader=group_leader)
		else:
			if group_leader:
				return render_template('end_voting.html', page = page, crew_id = crew_id)
			# regular user has to wait for the group leader to request final result
			else:
				while True:
					selected_restaurantID = sql_query(GET_CREW_SELECTED_REST, params=(crew_id,))[0]
					if selected_restaurantID != None:
						restaurant = sql_query(GET_RESTID_INFO, params=selected_restaurantID)[0]
						return render_template('results.html', page = page, restaurant = restaurant)
					sleep(5)

# user votes against restaurant - proceed to next restaurant or wait for results to appear
@app.route('/voteagainst', methods = ["GET", "POST"])
def vote_against():
	page = {'author': 'hello'}
	if request.method == "GET":
		return redirect(url_for("index"))
	if request.method == "POST":
		form = request.form
		crew_id = int(form["crew_id"])
		index = int(form["index"]) + 1
		restaurants = sql_query(GET_RESTAURANT_IDS, params=(crew_id,))
		group_leader = form["group_leader"]
		if index < len(restaurants) - 1:
			restaurant = sql_query(GET_RESTID_INFO, params=restaurants[index])[0]
			restaurant_dict = {"restaurant_id": restaurant[0], "name": restaurant[1], "cuisine": restaurant[2], "address": restaurant[3], "rating": restaurant[4], "price_range": restaurant[5], "menu_url": restaurant[6]}
			return render_template('voting.html', page = page, crew_id = crew_id, restaurant=restaurant_dict, index=index, group_leader=group_leader)
		else:
			if group_leader:
				# have a end voting button that will take you to the results page
				return render_template('end_voting.html', page = page, crew_id = crew_id)
			# regular user has to wait for the group leader to request final result
			else:
				while True:
					selected_restaurantID = sql_query(GET_CREW_SELECTED_REST, params=(crew_id,))[0]
					if selected_restaurantID != None:
						restaurant = sql_query(GET_RESTID_INFO, params=selected_restaurantID)[0]
						return render_template('results.html', page = page, restaurant = restaurant)
					sleep(5)

# Finds the selected restaurant after the group leader requests results
@app.route('/endvoting', methods = ["GET", "POST"])
def end_voting():
	page = {'author': 'hello'}
	if request.method == "GET":
		return redirect(url_for("index"))
	if request.method == "POST":
		form = request.form
		crew_id = int(form["crew_id"])
		selected_restaurantID = sql_query(SELECTED_RESTAURANT, params=(crew_id,))[0]
		sql_execute(UPDATE_CREW_SELECTED_RESTAURANT, (selected_restaurantID, crew_id))
		restaurant = sql_query(GET_RESTID_INFO, params=selected_restaurantID)[0]
		# remove crew-related info from the database
		voteIDS = sql_execute(GET_CREW_VOTES, params=(crew_id,))
		for voteID in voteIDs:
			sql_execute(DELETE_CREW_VOTES, params=voteID)
		sql_execute(DELETE_CREW, params=(crew_id,))
		return render_template('results.html', page = page, restaurant = restaurant)
		
# Main method
if __name__ == '__main__':
	app.run(**config['app'])
