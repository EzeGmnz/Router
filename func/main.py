''' Main nexus of modules'''

import numpy as np
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from .retrieve import *
from .pathoptimizer import *

FILE_PATH = "D:/Eze/Programacion/Router/SimpleServer/sandbox/src/planet_-62.291_-38.723_c4ce7a27.osm"
G = ox.core.graph_from_file(FILE_PATH, bidirectional=False, simplify=True, retain_all=False, name='unnamed')

def getRoute(starting_point, points):
	# Check if points are addresses, if so, we need to geocode
	full_coordinates = []

	if isinstance(points[0], str):
		# geocode
		full_coordinates = geocode(points)
		full_coordinates = geocode([starting_point]) + full_coordinates
	else:
		full_coordinates = points.copy()
		full_coordinates.insert(0, starting_point)

	distances, routes = retrieveDistanceMatrix(G, full_coordinates)

	# Again, starting point is on index 0
	best_route_indexes = optimumPath(0, distances)

	best_route = []
	best_route_length = 0
	for i, x in enumerate(best_route_indexes):
		if i < len(best_route_indexes) - 1:
			best_route_length += distances[x][best_route_indexes[i+1]]
			best_route.extend(routes[x][best_route_indexes[i + 1]])

	return best_route, best_route_length