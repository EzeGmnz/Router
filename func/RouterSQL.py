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

		# Building SQL Query
		query = 'select length, lat, lon, o_lat, o_lon from routeBetweenShell('
		latitudes = []
		longitudes = []

		for c in coordinates:
			latitudes.append(c[0])
			longitudes.append(c[1])

		query += 'ARRAY' + str(latitudes) + ','
		query += 'ARRAY' + str(longitudes) + ')'

		# execute query in PostreSQL database
		output = self.db.engine.execute(query)

		# Formatting output
		route = []
		orderedRoute = []
		length = 0

		for r in output:
			coord = (float(r['lat']), float(r['lon']))
			o_coord = (r['o_lat'], r['o_lon'])

			# found original coordinates
			if o_coord[0] is not None:
				if o_coord not in orderedRoute:
					orderedRoute.append(o_coord)

			l = r['length']
			if coord is not None and l is not None:
				route.append(coord)
				length += float(r['length'])
		
		return route, list(orderedRoute), length
