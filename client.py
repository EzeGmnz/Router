import requests
from flask import jsonify

URL = 'http://127.0.0.1:5000'

addresses = [
	'Paraguay 555, Bahia Blanca, Argentina',
	'Zapiola 1000, Bahia Blanca, Argentina',
	'Alem 1000, Bahia Blanca, Argentina']


'''JSON2 = {'points' : [
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
}'''

JSON = {'addresses': addresses}
r = requests.post(URL + '/routing', json = JSON)
if r.ok:
	result = r.json()
	success = result['result']
	if success == 'success':
		# Success
		print('length: ' + str(result['length']))
		print('route: ' + str(result['route']))
		print('ordered: ' + str(result['orderedCoords']))
	else:
		print('FAILED. Reason: ' + result['message'])
		# Failed
