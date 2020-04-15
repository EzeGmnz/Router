import requests
from flask import jsonify
import osmnx as ox

URL = 'http://127.0.0.1:5000'

JSON = {
	'start': 'Paraguay 555, Bahia Blanca, Argentina',
	'points' : ['Zapiola 200, Bahia Blanca, Argentina',
	'Uruguay 300, Bahia Blanca, Argentina',
	'Zapiola 700, Bahia Blanca, Argentina',
	'Alem 800, Bahia Blanca, Argentina',
	'Alem 1100, Bahia Blanca, Argentina',
	'Alem 50, Bahia Blanca, Argentina',
	'Estomba 350, Bahia Blanca, Argentina',
	'Paraguay 110, Bahia Blanca, Argentina',
	'Berutti 185, Bahia Blanca, Argentina',
	'Alvarado 230, Bahia Blanca, Argentina']
}

r = requests.post(URL + '/routing', json=JSON)
if r.ok:
	best_route = r.json()
	FILE_PATH = "D:/Eze/Programacion/Router/SimpleServer/sandbox/src/planet_-62.291_-38.723_c4ce7a27.osm"
	G = ox.core.graph_from_file(FILE_PATH, bidirectional=False, simplify=True, retain_all=False, name='unnamed')

	# Plotting
	fig, ax = ox.plot_graph_route(G, best_route)
	#fig, ax = ox.plot_graph_route(G, best_route, show=False, close=False)
	#for x in points:
	#	ax.scatter(x[1], x[0], c = 'red')
	#plt.show()