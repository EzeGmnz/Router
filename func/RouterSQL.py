#!/usr/bin/env python
"""
Router with PostgreSQL implementation

Allows input as either coordinates or physical addresses
"""

from flask_sqlalchemy import SQLAlchemy
from .IRouter import IRouter

__author__ = "Ezequiel Giménez"
__copyright__ = "Copyright 2020, Router project"
__credits__ = ["Ezequiel Giménez"]
__maintainer__ = "Ezequiel Giménez"
__email__ = "eze.gimenez.98@gmail.com"
__status__ = "Development"

class RouterSQL(IRouter):

	def __init__(self, database):
		self.db = database

	def getRoute(self, coordinates):
		
		query = 'select length, lat, lon, o_lat, o_lon from routeBetweenShell('
		latitudes = []
		longitudes = []

		for c in coordinates:
			latitudes.append(c[0])
			longitudes.append(c[1])

		query += 'ARRAY' + str(latitudes) + ','
		query += 'ARRAY' + str(longitudes) + ')'

		output = self.db.engine.execute(query)

		route = []
		orderedRoute = set()
		length = 0

		for r in output:
			coord = (float(r['lat']), float(r['lon']))
			o_lat = r['o_lat']
			o_lon = r['o_lon']

			if o_lat is not None and o_lon is not None:
				orderedRoute.add((float(o_lat), float(o_lon)))

			l = r['length']
			if coord is not None and l is not None:
				route.append(coord)
				length += float(r['length'])
		
		return route, list(orderedRoute), length
