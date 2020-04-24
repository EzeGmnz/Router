import requests
from flask import jsonify

URL = 'http://127.0.0.1:5000'

JSON1 = {'points' : [
	'Paraguay 555, Bahia Blanca, Argentina',
	'Zapiola 200, Bahia Blanca, Argentina',
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

JSON2 = {'points' : [
		[-38.706225, -62.265388],
		[-38.704577, -62.272677],
		[-38.704718, -62.27653],
		[-38.706823, -62.271098],
		[-38.712674, -62.270221],
		[-38.719969, -62.268381],
		[-38.719758, -62.25299],
		[-38.710612, -62.255185],
		[-38.716506, -62.272909],
		[-38.695943, -62.215489],
		[-38.780062, -62.267788],
		[-38.710363, -62.325136],
		[-38.750126, -62.178358]]
}

r = requests.post(URL + '/routing', json=JSON2)
if r.ok:
	best_route = r.json()
	print(best_route)
	