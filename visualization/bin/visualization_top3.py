import geopy

from geopy.geocoders import Nominatim

import certifi
import ssl

import json

import sys

import geopy.geocoders

import folium

from utils import timenorm

from collections import defaultdict

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

geopy.geocoders.options.default_user_agent = 'my_app/1'

geopy.geocoders.options.default_timeout = 7

geolocator = Nominatim()

with open(sys.argv[1], "r") as json_data:
	data = json.load(json_data, strict = False)

result = defaultdict(dict)
num_sup = 0
num_neg = 0
num_sup_loc = 0
num_neg_loc = 0

for k in data.keys():
	if ("__label__UNRELATED" not in data[k]["label"]):
		
		if ("__label__NEGATE" in data[k]["label"]):
			num_neg += 1
		else:
			num_sup += 1

		if ("time" in list(data[k].keys()) and len(list(data[k]["time"])) > 0):
			time = timenorm.era_to_era(max(data[k]["time"], key = data[k]["time"].get))
			
			if ("location" in list(data[k].keys()) and len(list(data[k]["location"])) > 3):
				
				if ("__label__NEGATE" in data[k]["label"]):
					num_neg_loc += 1
				else:
					num_sup_loc += 1
				
				loc_dict = data[k]["location"]
				new_loc = dict(sorted(loc_dict.items(), key=lambda x: x[1], reverse=True)[:3])

				for l in new_loc:
					if (l not in result[time]):
						result[time][l] = defaultdict(int)	
					if ("__label__NEGATE" in data[k]["label"]):
						result[time][l]["NEGATE"] += 1
					else:
						result[time][l]["SUPPORT"] += 1
					


			elif ("location" in list(data[k].keys()) and len(list(data[k]["location"])) > 0):

				if ("__label__NEGATE" in data[k]["label"]):
					num_neg_loc += 1
				else:
					num_sup_loc += 1
				
				location = max(data[k]["location"], key = data[k]["location"].get)
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
	m = folium.Map(location = [20, 0], tiles = "OpenStreetMap", zoom_start=2)
	print("///", time, "///")
	print()
	for loc in result[time].keys():
		if (loc):
			
			if (geolocator.geocode(loc)):
				location = [geolocator.geocode(loc).latitude, geolocator.geocode(loc).longitude]
				popup = loc 
				
				if (result[time][loc]["NEGATE"]):
					radius = int(result[time][loc]["NEGATE"]) * 200000
					popup = "%s, %s" % (popup, result[time][loc]["NEGATE"])
					folium.Circle(
						location = location,
						popup = popup,
						radius = radius,
						color = 'crimson',
						fill = True,
						fill_color = 'crimson'
						).add_to(m)
				else:
					radius = int(result[time][loc]["SUPPORT"]) * 200000
					popup = "%s, %s" % (popup, result[time][loc]["SUPPORT"])
					folium.Circle(
						location = location,
						popup = popup,
						radius = radius,
						color = 'green',
						fill = True,
						fill_color = 'green'
						).add_to(m)
	filename = "../maps/top3/" + time + ".html"
	m.save(filename)

print("===================")
print("DONE")
print("===================")