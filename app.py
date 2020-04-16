from flask import Flask, jsonify, request
import func.main as Main

app = Flask(__name__)

@app.route('/routing', methods=['GET', 'POST'])
def routing():
	content = request.json
	starting_point = content['start']
	points = content['points']
	routeR, coords, lengthR = Main.getRoute(starting_point, points)

	return jsonify(route= routeR, coordinates = coords, length = lengthR)

# Run locally
if __name__ == '__main__':
	app.run(host= '0.0.0.0', debug=True)
	