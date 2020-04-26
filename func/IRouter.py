#!/usr/bin/env python
"""
Router Interface
"""

__author__ = "Ezequiel Giménez"
__copyright__ = "Copyright 2020, Router project"
__credits__ = ["Ezequiel Giménez"]
__maintainer__ = "Ezequiel Giménez"
__email__ = "eze.gimenez.98@gmail.com"
__status__ = "Development"

class IRouter:

	def __init__(self):
		self.geocoder = geocoder

	'''
	input: coordinates: (lat, long) list for TSP
	output:	route: route as (lat, long) list
			coords: list with ordered input coordinates
			length: length in meters of the entire route
	'''
	def getRoute(self, coordinates):
		raise NotImplementedError