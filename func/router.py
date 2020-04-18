'''  '''

import numpy as np
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from .retrieve import *
from .database import *
from .pathoptimizer import *

class Router:

	def __init__(self):
		self._database = Database(["D:/Eze/Programacion/Router/SimpleServer/sandbox/src/planet_-62.291_-38.723_c4ce7a27.osm"])
		self._retriever = Retriever(self._database)
		self._path_optimizer = PathOptimizer(PathOptimizer.CLOSEST_NEIGHBOR)

	def getRouteFromAddresses(addresses):
		coordinates = []
		for a in addresses:
			coordinates.append(self._retriever(geocode(a)))
		return getRouteFromCoordinates(coordinates)

	# returns the best route (in coordinates) connecting all those points
	# the coordinates, the coordinates in order and the routes length
	def getRouteFromCoordinates(coordinates):
		distance_matrix, routes = self._retriever.distanceMatrix(coordinates)

		# Again, starting point is at index 0
		best_route_indexes = self._path_optimizer.optimumPath(0, distance_matrix)

		best_route = []
		best_route_length = 0
		for i, x in enumerate(best_route_indexes):
			if i < len(best_route_indexes) - 1:
				best_route_length += distance_matrix[x][best_route_indexes[i+1]]
				best_route.extend(routes[x][best_route_indexes[i + 1]])

		ordered_coordinates = []

		for coord in best_route:
			if coord in coordinates:
				ordered_coordinates.append(coord)

		return best_route, ordered_coordinates, best_route_length
