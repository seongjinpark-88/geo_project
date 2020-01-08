import geopy

from geopy.geocoders import Nominatim

import certifi
import ssl

ctx = ssl.create_default_context(cafile=certifi.where())

geopy.geocoders.options.default_ssl_context = ctx

geolocator = Nominatim()

location = geolocator.geocode("Tethyan")
print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))