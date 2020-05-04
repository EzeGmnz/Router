#!/usr/bin/env python
"""
Router with PostgreSQL implementation

Allows input as either coordinates or physical addresses
"""

from flask_sqlalchemy import SQLAlchemy
from math import radians, cos, sin, asin, sqrt

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

	def haversine(coord1, coord2):
		lat1, lon1 = coord1
		lat2, lon2 = coord2

		# convert decimal degrees to radians 
		lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

		# haversine formula 
		dlon = lon2 - lon1 
		dlat = lat2 - lat1 
		a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
		c = 2 * asin(sqrt(a)) 
		r = 6371 # Radius of earth in kilometers. Use 3956 for miles
		return c * r

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
			l = r['length']
			if l is not None: 
				length += float(l)

			# found original coordinates
			if o_coord[0] is not None:
				if o_coord not in orderedRoute:
					orderedRoute.append(o_coord)
				route.append(o_coord)
				route.append(coord)
			else:
				if coord is not None:
					route.append(coord)
		
		return route, list(orderedRoute), length

'''for i, r in enumerate(output):
			coord = (float(r['lat']), float(r['lon']))
			o_coord = (float(r['o_lat']), float(r['o_lon']))
			l = r['length']

			if o_coord is not None and coord is not None and l is not None:
				# found original coordinates	
				length += float(l)

				# adding o_coord to orderedRoute
				if o_coord not in orderedRoute:
					orderedRoute.append(o_coord)

				if i < output.rowcount - 1:
					# has next point
					x = 1
					nextCoord = None
					while nextCoord is None and i+x < output.rowcount:
						nextCoord = (float(output[i+x]['lat']),
									 float(output[i+x]['lon']))
						x += 1

					if nextCoord is not None:
						if haversine(o_coord, nextCoord) < haversine(coord, nextCoord):
							# o_coord is nearer to the next coord
							route.append(o_coord)

						else:
							# coord is nearer to the next coord
							route.append(o_coord)
							route.append(coord)
					else:
						pass
						# no next coord found
				else:
					# doesnt have next point
					x = 1
					prevCoord = None
					while prevCoord is None and i-x >= 0:
						prevCoord = (float(output[i-x]['lat']),
									 float(output[i-x]['lon']))
						x += 1

					if prevCoord is not None:
						if haversine(o_coord, prevCoord) < haversine(coord, prevCoord):
							# o_coord is nearer to the prev coord
							route.append(o_coord)
						else:
							# coord is nearer to the prev coord
							route.append(coord)
							route.append(o_coord)
					else:
						# no previous coord found
						pass
						
			else:
				# didnt find original coordinates
				route.append(coord)
				length += float(l)'''