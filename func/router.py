#!/usr/bin/env python
"""
Main coordinator
"""

from flask_sqlalchemy import SQLAlchemy
from geopy.geocoders import Nominatim

__author__ = "Ezequiel Giménez"
__copyright__ = "Copyright 2020, Router project"
__credits__ = ["Ezequiel Giménez"]
__maintainer__ = "Ezequiel Giménez"
__email__ = "eze.gimenez.98@gmail.com"
__status__ = "Development"

class Router:

	GEOCODER_TIMEOUT = 10

	def __init__(self, database):
		self.db = database
		self.geocoder = Nominatim(user_agent=__author__)

	def getRouteFromAddresses(self, addresses):
		aux = []
		for a in addresses:
			x = self._geocode(a)
			print(a, x)
			aux.append(x)
		return self.getRouteFromCoordinates(aux)

	# may need use nominatim
	def _geocode(self, address):
		coords = self.geocoder.geocode(address, timeout = self.GEOCODER_TIMEOUT)
		if coords is not None:
			return (coords.latitude, coords.longitude)
		else:
			return None

	# input: addresses: list of coordinates to visit
	# startin point is at index 0
	def getRouteFromCoordinates(self, coordinates):
		
		query = 'select length, lat, lon from routeBetweenShell('
		latitudes = []
		longitudes = []

		for c in coordinates:
			latitudes.append(c[0])
			longitudes.append(c[1])

		query += 'ARRAY' + str(latitudes) + ','
		query += 'ARRAY' + str(longitudes) + ')'

		output = self.db.engine.execute(query)

		aux = []
		for r in output:
			aux.append((float(r['lat']), float(r['lon'])))
		
		return (None, None, aux)
