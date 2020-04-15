'''
Access and transformation of data
All network related functionality
All geocoding related functionality
'''
import osmnx as ox
import networkx as nx
from xml.dom import minidom

FILE_PATH = "D:/Eze/Programacion/Router/SimpleServer/sandbox/src/planet_-62.291_-38.723_c4ce7a27.osm"

# v1 & v2 are the proximate points to X
# z is the st number to aproximate its lat lon
def _aproximate(v1, v2, z):
	x1,y1,z1 = v1
	x2,y2,z2 = v2

	lat = ((z - z1)/(z2-z1))*(x2-x1)+x1
	lon = ((z - z1)/(z2-z1))*(y2-y1)+y1

	return lat, lon

''' offline geocoder'''
# TODO determine a convention for address naming including town, state...
def geocode(addresses):
	xml = minidom.parse(FILE_PATH)
	itemlist = xml.getElementsByTagName('node')

	# list of tuples [street, number, town, country]
	# [[Paraguay, 555, BahiaBlanca, Argentina], [Zapiola, 200, BahiaBlanca, Argentina]]
	addresses_list = []

	for x in addresses:
		y = x.replace(',',' ')
		addresses_list.append(y.split(' '))

	# key = street name, value = dictionary (key: number, value: lat long)
	# {Paraguay : {	500 : (lat, lon),
	#				600 : (lat, lon)}}
	streets_looking_for = {x[0]:{} for x in addresses_list}

	for i, item in enumerate(itemlist):
		childs = item.getElementsByTagName('tag')
		# if its a street then it must have two child nodes
		# one for street name and another for its number
		street = None
		number = None

		for z in childs:
			if 'street' in z.getAttribute('k'):
				street = z.getAttribute('v')
			elif 'number' in z.getAttribute('k'):
				number = z.getAttribute('v')

			if number is not None and street is not None:
				for z in addresses_list:
					# check if the node corresponds to a street we are looking for
					# z[0] contains the street name
					# TODO check if doesnt find

					# TODO improve comparison method, to allow e.g "avenida" etc
					if z[0] in street:
						streets_looking_for[z[0]][int(float(number.split(' ')[0]))] = (float(item.getAttribute('lat')), float(item.getAttribute('lon')))
				break

	output = []
	for x in addresses_list:
		current_dict = streets_looking_for[x[0]]
		# find Y (smaller) & Z (larger)
		Y, Z = None, None
		X = int(x[1])
		Y_dist= float("inf")
		Z_dist = -float("inf")
		exact = False
		for j in current_dict.keys():
			result = X - j
			if result == 0:
				# found the exact coordinates
				output.append(current_dict[j])
				exact = True
				break
			if result >= 0 and result < Y_dist:
				Y = j
				Y_dist = result
			if result <= 0 and result > Z_dist:
				Z = j
				Z_dist = result

		if not exact:
			latY, lonY = current_dict[Y]
			latZ, lonZ = current_dict[Z]

			output.append(_aproximate((latY, lonY, Y), (latZ, lonZ, Z), X))

	return output
	# TODO use Y Z accordingly

# G: osmnx multidigrpah
# points: coordinates to visit
def retrieveDistanceMatrix(G, points):
	routes = [[[] for i in range(len(points))] for j in range(len(points))]
	distances = [[0 for i in range(len(points))] for j in range(len(points))]
	
	for i in range(len(points)):
		for j in range(len(points)):
			if i != j:
				origin = ox.get_nearest_node(G, points[i])
				end = ox.get_nearest_node(G, points[j])
				
				route = nx.shortest_path(G, origin, end, weight='length')
				distance = nx.shortest_path_length(G, origin, end, weight='length')
				routes[i][j] = route
				distances[i][j] = distance
			else:
				routes[i][j] = []
				distances[i][j] = float("inf")

	return distances, routes