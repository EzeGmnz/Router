from flask import Flask, jsonify, request
import func.main as Main

app = Flask(__name__)

@app.route('/routing', methods=['GET', 'POST'])
def routing():
	content = request.json
	starting_point = content['start']
	points = content['points']

	route, length = Main.getRoute(starting_point, points)

	# Need to format output as int to send json
	# otherwise raises a warning related to numpy's int64 ???
	aux = []
	for x in route:
		aux.append(int(x))
	return jsonify(aux)

# Run locally
if __name__ == '__main__':
	app.run(host= '0.0.0.0', debug=True)