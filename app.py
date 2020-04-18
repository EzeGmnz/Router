from flask import Flask, jsonify, request
from func.router import *

app = Flask(__name__)

@app.route('/routing', methods=['GET', 'POST'])
def routing():
	content = request.json
	starting_point = content['start']
	points = content['points']
	router = Router()

	routeR, coords, lengthR = router.getRouteFromAddresses(starting_point, points)

	return jsonify(route = routeR, coordinates = coords, length = lengthR)

# Run locally
if __name__ == '__main__':
	app.run(host= '0.0.0.0', debug=True)
	