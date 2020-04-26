#!/usr/bin/env python
"""
Geocoder implementation with Nominatim
"""

from geopy.geocoders import GeocodeFarm, Nominatim
from .IGeocoder import IGeocoder
from .Photon import Photon

__author__ = "Ezequiel Giménez"
__copyright__ = "Copyright 2020, Router project"
__credits__ = ["Ezequiel Giménez"]
__maintainer__ = "Ezequiel Giménez"
__email__ = "eze.gimenez.98@gmail.com"
__status__ = "Development"

class GeocoderMultiple(IGeocoder):

	GEOCODER_TIMEOUT = 10

	def __init__(self):
		self.geocoders = [Photon(), GeocodeFarm(), Nominatim()]

	def geocode(self, address):

		i = 0
		coord = None
		while i < len(self.geocoders) and coord is None:
			coord = self.geocoders[i].geocode(address, timeout = self.GEOCODER_TIMEOUT)
			
		if coord is not None:
			print(address, (coord.latitude, coord.longitude))
			return (coord.latitude, coord.longitude)
		else:
			return None

