import geopy

from geopy.geocoders import Nominatim

import certifi
import ssl

import json

import geopy.geocoders

import folium

from utils import timenorm

from collections import defaultdict

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

geopy.geocoders.options.default_user_agent = 'my_app/1'

geopy.geocoders.options.default_timeout = 7

geolocator = Nominatim()

with open("../data/new_result.json", "r") as json_data:
	data = json.load(json_data, strict = False)

# print(data)

result = defaultdict(dict)

for k in data.keys():
	if ("__label__UNRELATED" not in data[k]["label"]):
		
		if ("location" in list(data[k].keys()) and len(list(data[k]["location"])) > 0):
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

print(result)

# for time in result.keys():
	# print(time, len(result[time]))

# for time in result.keys():
# 	m = folium.Map(location = [20, 0], tiles = "OpenStreetMap", zoom_start=2)

# 	for loc in result[time].keys():
# 		if (loc):
# 			# print(loc)
# 			if (geolocator.geocode(loc)):
# 				location = [geolocator.geocode(loc).latitude, geolocator.geocode(loc).longitude]
# 				popup = loc 
				
# 				if (result[time][loc]["NEGATE"]):
# 					radius = int(result[time][loc]["NEGATE"]) * 100000
# 					popup = "%s, %s" % (popup, result[time][loc]["NEGATE"])
# 					folium.Circle(
# 						location = location,
# 						popup = popup,
# 						radius = radius,
# 						color = 'green',
# 						fill = True,
# 						fill_color = 'green'
# 						).add_to(m)
# 				else:
# 					radius = int(result[time][loc]["SUPPORT"]) * 100000
# 					popup = "%s, %s" % (popup, result[time][loc]["SUPPORT"])
# 					folium.Circle(
# 						location = location,
# 						popup = popup,
# 						radius = radius,
# 						color = 'crimson',
# 						fill = True,
# 						fill_color = 'crimson'
# 						).add_to(m)
# 	filename = "../maps/" + time + ".html"
# 	m.save(filename)

# for time in result.keys():
	# m = folium.Map(location = [20, 0])

		# Keymax = max(Tv, key=Tv.get) 
		# print(data[k])

# location = geolocator.geocode("Tucson")
# print(location)
# print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))