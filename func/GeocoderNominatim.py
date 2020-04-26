#!/usr/bin/env python
"""
Geocoder implementation with Nominatim
"""

from geopy.geocoders import Nominatim
from .IGeocoder import IGeocoder

__author__ = "Ezequiel Giménez"
__copyright__ = "Copyright 2020, Router project"
__credits__ = ["Ezequiel Giménez"]
__maintainer__ = "Ezequiel Giménez"
__email__ = "eze.gimenez.98@gmail.com"
__status__ = "Development"

class GeocoderNominatim(IGeocoder):

	GEOCODER_TIMEOUT = 10

	def __init__(self):
		self.geocoder = Nominatim(user_agent = __author__)

	def geocode(self, address):
		coords = self.geocoder.geocode(address, timeout = self.GEOCODER_TIMEOUT)
		if coords is not None:
			return (coords.latitude, coords.longitude)
		else:
			return None