#!/usr/bin/env python
"""
Geocoder implementation with Nominatim
"""

from geopy.geocoders import Nominatim
from .IGeocoder import IGeocoder
import requests

__author__ = "Ezequiel Giménez"
__copyright__ = "Copyright 2020, Router project"
__credits__ = ["Ezequiel Giménez"]
__maintainer__ = "Ezequiel Giménez"
__email__ = "eze.gimenez.98@gmail.com"
__status__ = "Development"

class Photon:
	PHOTON_URL = 'http://photon.komoot.de/api/?q='

	class Location:
		def __init__(self, lat, lon):
			self.latitude = lat
			self.longitude = lon

	GEOCODER_TIMEOUT = 10

	def __init__(self):
		self.geocoder = Nominatim(user_agent = __author__)

	def geocode(self, address, timeout = 1):
		url = self.PHOTON_URL + address.replace(' ', '%20')
		r = requests.get(url, timeout = timeout)

		if r.ok:
			json = r.json()
			features = json['features']
			for x in features:
				if "geometry" in x:
					return self.Location(x['geometry']['coordinates'][1], x['geometry']['coordinates'][0])
		else:
			return None