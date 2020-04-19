#!/usr/bin/env python
"""
Main coordinator
"""
import numpy as np
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from .retrieve import *
from .database import *
from .pathoptimizer import *
import time

__author__ = "Ezequiel Giménez"
__copyright__ = "Copyright 2020, Router project"
__credits__ = ["Ezequiel Giménez"]
__maintainer__ = "Ezequiel Giménez"
__email__ = "eze.gimenez.98@gmail.com"
__status__ = "Development"

class Router:

	def __init__(self):
		self._database = Database(["D:/Eze/Programacion/Router/SimpleServer/sandbox/src/planet_-62.291_-38.723_c4ce7a27.osm"])
		self._retriever = Retriever(self._database)
		self._path_optimizer = PathOptimizer(PathOptimizer.CLOSEST_NEIGHBOR)

	def getRouteFromAddresses(self, addresses):
		
		###TODO
		start = time.perf_counter()
		print("START\tgetRouteFromAddresses ", time.perf_counter())
		###

		###TODO
		start1 = time.perf_counter()
		print("START\tgeocode ", time.perf_counter())
		###

		coordinates = []
		for a in addresses:
			coordinates.append(self._retriever.geocode(a))

		###
		end1 = time.perf_counter()
		print("END\tgeocode", time.perf_counter(), " - " , end1-start1)
		###

		###
		end = time.perf_counter()
		print("END\tgetRouteFromAddresses", time.perf_counter(), " - " , end-start)
		###

		return self.getRouteFromCoordinates(coordinates)

	# returns the best route (in coordinates) connecting all those points
	# the coordinates, the coordinates in order and the routes length
	def getRouteFromCoordinates(self, coordinates):

		###TODO
		start = time.perf_counter()
		print("START\tgetRouteFromCoordinates ", time.perf_counter())
		###

		# Getting windy distance matrix
		distance_matrix, routes = self._retriever.distanceMatrix(coordinates)

		# Again, starting point is at index 0
		best_route_indexes = self._path_optimizer.optimumPath(0, distance_matrix)

		best_route = []
		best_route_length = 0
		for i, x in enumerate(best_route_indexes):
			if i < len(best_route_indexes) - 1:
				best_route_length += distance_matrix[x][best_route_indexes[i+1]]
				best_route.extend(routes[x][best_route_indexes[i + 1]][:-1])

		ordered_coordinates = []

		for coord in best_route:
			if coord in coordinates:
				ordered_coordinates.append(coord)

		###
		end = time.perf_counter()
		print("END\tgetRouteFromCoordinates", time.perf_counter(), " - " , end-start)
		###

		return best_route, ordered_coordinates, best_route_length
