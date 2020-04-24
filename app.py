#!/usr/bin/env python
"""
Flask app implementation 
"""
from flask import Flask, jsonify, request
from func.router import *
from flask_sqlalchemy import SQLAlchemy

__author__ = "Ezequiel Giménez"
__copyright__ = "Copyright 2020, Router project"
__credits__ = ["Ezequiel Giménez"]
__maintainer__ = "Ezequiel Giménez"
__email__ = "eze.gimenez.98@gmail.com"
__status__ = "Development"

app = Flask(__name__)
db = SQLAlchemy()

POSTGRES = {
    'user': 'postgres',
    'pw': 'eolche28',
    'db': 'osm',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_app(app)

@app.route('/routing', methods=['GET', 'POST'])
def routing():
	content = request.json
	points = content['points']

	router = Router(db)

	if isinstance(points[0], str):
		# if they are addresses
		routeR, coords, lengthR = router.getRouteFromAddresses(points)
	else:
		routeR, coords, lengthR = router.getRouteFromCoordinates(points)
	
	return jsonify(route = routeR, coord = coords, length = lengthR)

@app.route('/')
def index():
	return "Hello World!"

# Run locally
if __name__ == '__main__':
	app.run(host= '0.0.0.0', debug=True)
	