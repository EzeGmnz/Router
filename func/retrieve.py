'''
Access and transformation of data
All street network related functionality
All geocoding related functionality
'''
import osmnx as ox
import networkx as nx
from xml.dom import minidom

class Retriever:

	def __init__(database):
		self._database = database

	# v1 & v2 are the proximate coordinates to X
	# z is the st number to aproximate its lat lon
	def _aproximate(v1, v2, z):
		x1,y1,z1 = v1
		x2,y2,z2 = v2

		lat = ((z - z1)/(z2-z1))*(x2-x1)+x1
		lon = ((z - z1)/(z2-z1))*(y2-y1)+y1

		return lat, lon

	def _getNameAndNumberFromNode(node):
		tags = node.getElementsByTagName('tag')

		street, number = None, None
		i = 0
		while i < len(tags) and (street is None or number is None):
			if 'addr:street' == tags[i].getAttribute('k'):
				street = tags[i].getAttribute('v')
			elif 'addr:housenumber' == tags[i].getAttribute('k'):
				number = int(float(tags[i].getAttribute('v')))

		return street, number

	''' Geocoder; turns a physical address into coordinates'''
	# TODO May want to optimize if two or more addresses look into the same osm file
	def geocode(address):
		xml = minidom.parse(self._database.getSectionFromAddress(address))
		nodes = xml.getElementsByTagName('node')

		# Conventionally, street name will be at index 0 and number at 1
		address_as_list = address.replace(',',' ').split(' ')

		# finding nodes with coordinates in the proximity of the address
		Y, Z = None, None
		X = address_as_list[1]

		Y_dist = float("inf")
		Z_dist = -float("inf")

		for node in nodes:
			street, number = getNameAndNumberFromNode(node)

			# TODO improve comparison method
			if address_as_list[0] in street:
				# node belongs to the same street
				result = X - number
				if result == 0:
					# found the exact coordinate
					return (node.getAttribute(lat), node.getAttribute(lon))

				if result > 0 and result < Y_dist:
					Y = node
					Y_dist = result
				if result < 0 and result > Z_dist:
					Z = node
					Z_dist = result

		latY, lonY = Y.getAttribute(lat), Y.getAttribute(lon)
		latZ, lonZ = Z.getAttribute(lat), Z.getAttribute(lon)

		return _aproximate((latY, lonY, Y), (latZ, lonZ, Z), X)

	# G: osmnx multidigrpah
	# points: coordinates to visit
	# note that this alogrithm results in a windy matrix, that is,
	# non-symetrical, since the route from X to Y may not be the same route from Y to X
	def distanceMatrix(coordinates):
		# !!! TODO see how to join the osm files to where the coordinates belong
		# below code is an implementation assuming all belong to the same file

		FILE_PATH = self._database.getSectionFromCoordinate(coordinates[0])
		G = ox.core.graph_from_file(FILE_PATH, bidirectional=False, simplify=True, retain_all=False, name='unnamed')

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
					for node in node_route:
						route.append((G.nodes[node]['x'], G.nodes[node]['y']))
					
					routes[i][j] = route
					distances[i][j] = distance
				else:
					routes[i][j] = []
					distances[i][j] = float("inf")

		return distances, routes