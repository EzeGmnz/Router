#!/usr/bin/env python
"""
Flask app implementation 
"""
from flask import Flask, jsonify, request
from func.router import *

__author__ = "Ezequiel Giménez"
__copyright__ = "Copyright 2020, Router project"
__credits__ = ["Ezequiel Giménez"]
__maintainer__ = "Ezequiel Giménez"
__email__ = "eze.gimenez.98@gmail.com"
__status__ = "Development"

app = Flask(__name__)

@app.route('/routing', methods=['GET', 'POST'])
def routing():
	content = request.json
	points = content['points']

	router = Router()
	routeR, coords, lengthR = router.getRouteFromAddresses(points)

	return jsonify(route = routeR, coordinates = coords, length = lengthR)

# Run locally
if __name__ == '__main__':
	app.run(host= '0.0.0.0', debug=True)
	