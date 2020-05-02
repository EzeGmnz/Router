import requests
from flask import jsonify

URL = 'http://127.0.0.1:5000'

addresses = [
	'Paraguay 555, Bahia Blanca, Argentina',
	'Zapiola 1000, Bahia Blanca, Argentina',
	'Alem 1000, Bahia Blanca, Argentina',
	'Horneros 20, Bahia Blanca, Argentina']

'''San Andres 300, Bahia Blanca, Argentina',
'Charlone 500, Bahia Blanca, Argentina',
'Parchappe 678, Bahia Blanca, Argentina',
'Pringles 1000, Bahia Blanca, Argentina',
'Chequen 20, Bahia Blanca, Argentina',
'Pellegrini 120, Bahia Blanca, Argentina',
'Brown 600, Bahia Blanca, Argentina',
'España 200, Bahia Blanca, Argentina']'''

JSON = {'addresses': addresses}
r = requests.post(URL + '/routing', json = JSON)
if r.ok:
	result = r.json()
	success = result['result']
	if success == 'success':
		# Success
		print('length: ' + str(result['length']))
		print('route: ' + str(result['route']))
		print('ordered coordinates: ' + str(result['orderedCoords']))
		print('ordered addresses: ' + str(result['orderedAddresses']))
	else:
		# Failed
		print('FAILED. Reason: ' + result['message'])