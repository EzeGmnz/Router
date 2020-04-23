#!/usr/bin/env python
'''
Access and transformation of data
All street network related functionality
All geocoding related functionality
'''

import osmnx as ox
from .utils import *
import networkx as nx
from xml.dom import minidom
from networkx.readwrite import json_graph
import json
import time

__author__ = "Ezequiel Giménez"
__copyright__ = "Copyright 2020, Router project"
__credits__ = ["Ezequiel Giménez"]
__maintainer__ = "Ezequiel Giménez"
__email__ = "eze.gimenez.98@gmail.com"
__status__ = "Development"

class Retriever:

	def __init__(self, database):
		self._database = database

	# v1 & v2 are the proximate coordinates to X
	# z is the st number to aproximate its lat lon
	def _aproximate(self, v1, v2, X):
		(latY,lonY),Y = v1
		(latZ,lonZ),Z = v2

		lat = ((X - Y)/(Z-Y))*(latZ-latY)+latY
		lon = ((X - Y)/(Z-Y))*(lonZ-lonY)+lonY

		return lat, lon

	''' Geocoder; turns a physical address into coordinates'''
	def geocode(self, address):

		# Conventionally, street name will be at index 0 and number at 1
		address_as_list = address.replace(',',' ').split(' ')

		# finding nodes with coordinates in the proximity of the address
		Y, Z = None, None
		nodeY, nodeZ = None,None
		X = int(address_as_list[1])

		Y_dist = float("inf")
		Z_dist = -float("inf")

		parsed_osm = self._database.get(self._database.getSectionFromAddress(address))

		# mapping inputed street name to osm file one
		real_street_name = None
		for s in parsed_osm.keys():
			if nameComparison(formatAddress(s), formatAddress(address_as_list[0]), 1):
				real_street_name = s

		# if street name exists in database
		if real_street_name is not None:
			# for each number belonging to the street
			for number, (lat, lon) in parsed_osm[real_street_name].items():
				print(parsed_osm[real_street_name])
				result = X - number
				if result == 0:
					# found the exact coordinate
					return (lat, lon)

				if result > 0 and result < Y_dist:
					nodeY = (lat, lon)
					Y = int(number)
					Y_dist = result
				if result < 0 and result > Z_dist:
					nodeZ = (lat, lon)
					Z = int(number)
					Z_dist = result
		else:
			# TODO see what to do if street name was not found
			print("NOT FOUND", address_as_list)

		return self._aproximate((nodeY, Y), (nodeZ, Z), X)

	# Returns multidigaph 'G'
	def _openGraph(self, filename):
		G = None
		try:
			with open(filename + 'graph', 'r') as file:
				G = json_graph.node_link_graph(json.load(file)) 
		except IOError:
			# writing graph's json
			G = ox.core.graph_from_file(filename, bidirectional=False, simplify=True, retain_all=False, name='unnamed')
			file = open(filename + 'graph', 'w+')
			print("aAAAAAAAAA", json_graph.node_link_data(G))
			file.write(json.dumps(json_graph.node_link_data(G)))
			file.close()
		return G

	# G: osmnx multidigrpah
	# points: coordinates to visit
	# note that this alogrithm results in a windy matrix, that is,
	# non-symetrical, since the route from X to Y may not be the same route from Y to X
	def distanceMatrix(self, coordinates):
		# !!! TODO see how to join the osm files to where the coordinates belong
		# below code assumes all coords belong to the same file as the starting point

		###TODO
		start = time.perf_counter()
		print("START\tdistancematrix ", time.perf_counter())
		###

		FILE_PATH = self._database.getSectionFromCoordinate(coordinates[0])
		G = self._openGraph(FILE_PATH)
		#G = ox.core.graph_from_file(FILE_PATH, bidirectional=False, simplify=True, retain_all=False, name='unnamed')
		
		routes = [[[] for i in range(len(coordinates))] for j in range(len(coordinates))]
		distances = [[0 for i in range(len(coordinates))] for j in range(len(coordinates))]		
		
		for i in range(len(coordinates)):
			for j in range(len(coordinates)):
				if i != j:
					origin = ox.get_nearest_node(G, coordinates[i])
					end = ox.get_nearest_node(G, coordinates[j])

					

					node_route = nx.shortest_path(G, origin, end, weight='length')
					distance = nx.shortest_path_length(G, origin, end, weight='length')
					
					
					# node to coordinates translation
					route = []

					for node in node_route[1:len(node_route)-1]:
						# dont add first and last (will be added later to match input coords)
						route.append((G.nodes[node]['y'], G.nodes[node]['x']))
					# adding starting and end coords
					route = [coordinates[i]] + route + [coordinates[j]]

					routes[i][j] = route
					distances[i][j] = distance
				else:
					routes[i][j] = []
					distances[i][j] = float("inf")
		

		###
		end = time.perf_counter()
		print("END\tdistancematrix", time.perf_counter(), " - " , end-start)
		###

		return distances, routes