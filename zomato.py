import requests, logger, urllib.request as urllib
from restaurant import restaurant 
from bs4 import BeautifulSoup

# API Keys
GEOCODING_API_KEY = "AIzaSyDS1s0wGheIZjQ-r_ZP1A6Y4YZ7tnyT_KQ"
ZOMATO_API_KEY = "fc913e8655ebbf9484b2ff4b896b6183"

# URLs for API Calls
GEOCODING = "https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={key}"
ZOMATO = "https://developers.zomato.com/api/v2.1/"

# Request headers for Zomato API
hdrs = {
		"User-agent": "curl/7.43.0",
        "Accept": "application/json",
        "Content-Type": 'application/json',
        "X-Zomato-API-Key": ZOMATO_API_KEY
	}

# Turns a zip code into a latitude and longitude
def toLatLong(zip):
	"""
	Takes in a zip code and returns the latitude and longitude associated with that zip code.

	:param zip: Zip Code
	:returns : tuple (lat, lng) where the lat is latitude and lng is longitude.

	"""
	url = GEOCODING.format(
		address = zip,
		key = GEOCODING_API_KEY
	)
	results = requests.get(url).json()
	if results["results"] == []: return []
	lat = results["results"][0]["geometry"]["location"]["lat"]
	lng = results["results"][0]["geometry"]["location"]["lng"]
	return (lat, lng)

def getCuisinesZip(zip):
	"""
	Takes in a zip code and returns the popular cuisines near the zip code.
	
	:param zip: Zip Code
	:returns: List of cuisine tuples (cuisine_name, id), where cuisine_name is the
			  English name of the cuisine and id is the cuisine_id used by the
			  Zomato API
	"""
	coords = toLatLong(zip)
	if coords == []: return coords
	lat = coords[0]
	lng = coords[1]
	geocode_url = ZOMATO + "geocode?lat=" + str(lat) + "&lon=" + str(lng)
	results = requests.get(geocode_url, headers = hdrs).json()
	cuisines = results["popularity"]["top_cuisines"]
	cuisine_ids = []
	cuisines_url = ZOMATO + "cuisines?lat=" + str(lat) + "&lon=" + str(lng)
	results = requests.get(cuisines_url, headers = hdrs).json()
	for cuisine in cuisines:
		for c in results["cuisines"]:
			if (c["cuisine"]["cuisine_name"] == cuisine):
				cuisine_ids.append((cuisine, c["cuisine"]["cuisine_id"]))
	return cuisine_ids

def getRestaurants(cuisine_ids, zip):
	"""
	Takes in a list of cuisine ids and a zip code and returns a list of restaurant objects

	:param cuisine_ids: List of cuisine_ids
	:param zip: Zip Code
	:returns: List of restaurant objects with the information needed to input to restaurant table
	"""
	coords = toLatLong(zip)
	lat = coords[0]
	lng = coords[1]
	cuisines_string = ""
	for c in cuisine_ids:
		cuisines_string += str(c[1]) + ","
	cuisines_string = cuisines_string[:len(cuisines_string) - 1]
	search_url = ZOMATO + "search?lat=" + str(lat) + "&lon=" + str(lng) + "&cuisines=" + cuisines_string + "&sort=real_distance&count=10"
	results = requests.get(search_url, headers = hdrs).json()
	
	# Restaurant Object List
	restaurants = results["restaurants"]
	restaurantObjs = []
	for n in restaurants:
		r = n["restaurant"]
		name = r["name"]
		cuisine = r["cuisines"]
		address = r["location"]["address"]
		rating = r["user_rating"]["aggregate_rating"]
		price_range = r["price_range"]
		menu_url = r["menu_url"]
		photo_album = r["photos_url"]
		image_url = getImageUrl(photo_album)
		rObj = restaurant(name, cuisine, address, rating, price_range, menu_url, image_url)
		restaurantObjs.append(rObj)
	return restaurantObjs

def getImageUrl(url):
	page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
	soup = BeautifulSoup(page.content, 'html.parser')
	thumbsContainer = soup.find(id="thumbsContainer")
	a = thumbsContainer.find("a")
	if a != None:
		url = a['href']
		page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
		soup = BeautifulSoup(page.content, 'html.parser')
		bigImage = soup.find(class_="big-image ui middle aligned one column centered grid")
		img = bigImage.find("img")
		return img['src']
	else:
		return ""