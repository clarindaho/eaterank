import requests, logger

GEOCODING_API_KEY = "AIzaSyDS1s0wGheIZjQ-r_ZP1A6Y4YZ7tnyT_KQ"
ZOMATO_API_KEY = "fc913e8655ebbf9484b2ff4b896b6183"

GEOCODING = "https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={key}"
ZOMATO = "https://developers.zomato.com/api/v2.1/"

hdrs = {
		"User-agent": "curl/7.43.0",
        "Accept": "application/json",
        "Content-Type": 'application/json',
        "X-Zomato-API-Key": ZOMATO_API_KEY
	}


def toLatLong(zip):
	url = GEOCODING.format(
		address = zip,
		key = GEOCODING_API_KEY
	)
	results = requests.get(url).json()
	lat = results["results"][0]["geometry"]["location"]["lat"]
	lng = results["results"][0]["geometry"]["location"]["lng"]
	return (lat, lng)

def getCusinesZip(zip):
	coords = toLatLong(zip)
	lat = coords[0]
	lng = coords[1]
	geocode_url = ZOMATO + "geocode?lat=" + str(lat) + "&lon=" + str(lng)
	print(geocode_url)
	results = requests.get(geocode_url, headers = hdrs).json()
	cuisines = results["popularity"]["top_cuisines"]
	cuisine_ids = []
	cuisines_url = ZOMATO + "cuisines?lat=" + str(lat) + "&lon=" + str(lng)
	results = requests.get(cuisines_url, headers = hdrs).json()
	for cuisine in cuisines:
		for c in results["cuisines"]:
			if (c["cuisine"]["cuisine_name"] == cuisine):
				cuisine_ids.append((cuisine, c["cuisine"]["cuisine_id"]))
	#print(results.text)
	#print(results.headers['content-type'])
	return cuisine_ids

"""
def getRestaurants(cuisine_ids, zip):
	coords = toLatLong(zip)
	lat = coords[0]
	lng = coords[1]
	cuisines_string = ""
	for c in cuisine_ids:
		cuisines_string += c[1] + ","
	cuisines_string = cuisines_string[:len(cuisines_string) - 1]
	print(cuisines_string)
	search_url = ZOMATO + "search?lat=" + str(lat) + "&lon=" + str(lng) + "&"
	return ""
"""

print(getRestaurants(getCusinesZip(11363), 11363))
