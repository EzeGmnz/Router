''' Heuristic for solving the windy TSP problem'''
from itertools import permutations

class PathOptimizer:

	CLOSEST_NEIGHBOR = 'closest_neighbor'
	PERMUTATIONS = 'permutations'

	def __init__(self, algorithm=CLOSEST_NEIGHBOR):
		self._algorithm = algorithm

	############# ALGORITHMS ################

	# Computes shortest route calculating all posible permutations
	# and returns the shortest one. 
	# Most accurate one but has a complexity time of N!
	# NOT PRACTICAL AT ALL
	# TODO optimize. Make sub route with k-mean approach
	def _permutations(starting_index, matrix):
		best_route = []
		min_distance = float("inf")

		nodes_index = [x for x in range(len(matrix[0]))]
		nodes_index.remove(starting_index)
		
		all_routes = permutations(nodes_index)

		for x in all_routes:
			current = list(x)
			current.insert(0, starting_index)
			current_distance = 0
			for i, y in enumerate(current):
				if i < len(current) - 1:
					current_distance += matrix[y][current[i + 1]]
			if current_distance < min_distance:
				min_distance = current_distance
				best_route = current

		return best_route

	# node_index: matrix index of node to find closest
	# matrix: distance matrix
	# visited: already visited nodes
	def _closest(node_index, matrix, visited):
		distance = float("inf")
		closest_index = None
		for x in range(len(matrix[0])):
			if x not in visited and matrix[node_index][x] < distance:
				closest_index = x
				distance = matrix[node_index][x]
		return closest_index

	# Computes shortest path using the nearest neighbor algorithm
	# TODO optimize with 2op
	# starting_index: starting index
	def _nearestNeighbor(starting_index, matrix):
		current = starting_index
		best_route = [starting_index]

		for x in range(len(matrix[0]) - 1):
			next_index = _closest(current, matrix, best_route)
			best_route.append(next_index)
			current = next_index

		return best_route
			

	#######################################

	# A: starting matrix index
	# matrix: distance matrix
	def optimumPath(A, matrix):
		if self._algorithm == CLOSEST_NEIGHBOR:
			return _nearestNeighbor(A, matrix)
		elif self._algorithm == PERMUTATIONS:
			return _permutations(A, matrix)
