import requests, logger

GEOCODING_API_KEY = "AIzaSyDS1s0wGheIZjQ-r_ZP1A6Y4YZ7tnyT_KQ"
ZOMATO_API_KEY = "fc913e8655ebbf9484b2ff4b896b6183"

GEOCODING = "https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={key}"
ZOMATO = "https://developers.zomato.com/api/v2.1"

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
	hdrs = {
		"User-agent": "curl/7.43.0",
        "Accept": "application/json",
        "Content-Type": 'application/json',
        "X-Zomato-API-Key": ZOMATO_API_KEY
	}
	coords = toLatLong(zip)
	lat = coords[0]
	lng = coords[1]
	url = ZOMATO + "cuisines?lat=" + str(lat) + "&lon=" + str(lng)
	print(url)
	results = requests.get(url, headers = hdrs)
	print(results.text)
	print(results.headers['content-type'])
	return results

print(getCusinesZip(11363))
