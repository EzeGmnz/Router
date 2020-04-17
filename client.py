import requests
from flask import jsonify

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
	print(r.json())
	