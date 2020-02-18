import sys 

import geopy
from geopy.geocoders import Nominatim
import geopy.geocoders

import certifi
import ssl

import json

import folium

from utils import timenorm

from collections import defaultdict

# load certificates for geocoder
ctx = ssl.create_default_context(cafile=certifi.where())

geopy.geocoders.options.default_ssl_context = ctx
geopy.geocoders.options.default_user_agent = 'my_app/1'
geopy.geocoders.options.default_timeout = 7

# load geolocator
geolocator = Nominatim()

# open the result file
with open(sys.argv[1], "r") as json_data:
	data = json.load(json_data, strict = False)

result = defaultdict(dict)

# count frequencies
for k in data.keys():
	if ("__label__UNRELATED" not in data[k]["label"]):
		
		if ("location" in list(data[k].keys()) and len(list(data[k]["location"])) > 3):
			location = max(data[k]["location"], key = data[k]["location"].get)
		else:
			location = ""
		if ("time" in list(data[k].keys()) and len(list(data[k]["time"])) > 0):
			time = timenorm.era_to_era(max(data[k]["time"], key = data[k]["time"].get))
		else:
			time = ""

		if (time):
			if (location not in result[time]):
				result[time][location] = defaultdict(int)	
			if ("__label__NEGATE" in data[k]["label"]):
				result[time][location]["NEGATE"] += 1
			else:
				result[time][location]["SUPPORT"] += 1


print("===================")
print("START creating MAPS")
print("===================")

for time in result.keys():
	
	# generate an empty map
	m = folium.Map(location = [20, 0], tiles = "OpenStreetMap", zoom_start=2)

	# print geological era
	print("///", time, "///")
	
	# iterate over locations
	for loc in result[time].keys():
		if (loc):
			# when the location is recognized
			if (geolocator.geocode(loc)):
				# get latitude and longitude
				location = [geolocator.geocode(loc).latitude, geolocator.geocode(loc).longitude]

				popup = loc 
				
				if (result[time][loc]["NEGATE"]):
					# set radius based on the frequency
					radius = int(result[time][loc]["NEGATE"]) * 200000
					# the popup info for the point
					popup = "%s, %s" % (popup, result[time][loc]["NEGATE"])
					# draw the circle
					folium.Circle(
						location = location,
						popup = popup,
						radius = radius,
						color = 'crimson',
						fill = True,
						fill_color = 'crimson'
						).add_to(m)
				else:
					# set radius based on the frequency
					radius = int(result[time][loc]["SUPPORT"]) * 200000
					# the popup info for the point
					popup = "%s, %s" % (popup, result[time][loc]["SUPPORT"])
					# draw the circle
					folium.Circle(
						location = location,
						popup = popup,
						radius = radius,
						color = 'green',
						fill = True,
						fill_color = 'green'
						).add_to(m)
	# save the map
	filename = "../maps/top1/" + time + ".html"
	m.save(filename)

print("===================")
print("DONE")
print("===================")

# for time in result.keys():
	# m = folium.Map(location = [20, 0])

		# Keymax = max(Tv, key=Tv.get) 
		# print(data[k])

# location = geolocator.geocode("Tucson")
# print(location)
# print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))