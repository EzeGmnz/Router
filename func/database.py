from xml.dom import minidom

''' Osm files accesing is done from here'''
class Database:

	''' files: file name list'''
	def __init__(self, files = None):
		if files is None:
			self._file_list = []
		else:
			self._file_list = files
		pass
		self._description_osm_map = {}

		for x in _file_list:
			self._description_osm_map[x] = _getFileDescription(minidom.parse(x))

	''' add a file to existing ones
	file: the file to add '''
	def addFile(self, file):
		self._file_list.append(file)
		if file not in self._description_osm_map:
			self._description_osm_map[file] = _getFileDescription(minidom.parse(file))
		pass

	# Returns the osm description as a map
	# the description includes: bounds(minlat, minlon, maxlat, maxlon), state/country/city name(name),
	# and 
	# file: minidom xml file
	def _getFileDescription(self, xml):
		output_map = {}
		
		# retrieving bounds
		bounds = xml.getElementsByTagName('bounds')
		if len(bounds) == 1:
			output_map['minlat'] = float(bounds[0].getAttribute('minlat'))
			output_map['minlon'] = float(bounds[0].getAttribute('minlon'))
			output_map['maxlat'] = float(bounds[0].getAttribute('maxlat'))
			output_map['maxlon'] = float(bounds[0].getAttribute('maxlon'))

		# retrieving name
		nodes = xml.getElementsByTagName('node')
		tags = nodes[0].getElementsByTagName('tag')

		i = 0
		while i < len(tags) and 'name' not in output_map or 'place' not in output_map:
			t = tags[i]
			if t.getAttribute('k') == 'name':
				output_map['name'] = t.getAttribute('v')
			elif t.getAttribute('k') == 'place':
				output_map['place'] = t.getAttribute('v')
			i += 1

		return output_map

	# TODO improve on how the states/cities are typen
	''' Return the first osm file holding the address, if exists, otherwise return None'''
	def getSectionFromAddress(self, address):
		for k, v in self._description_osm_map.items():
			if v['name'] in address:
				return k

	''' Return the first osm file holding the coordinate, if exists, otherwise return None'''
	def getSectionFromCoordinate(self, coordinate):
		lat, lon = coordinate
		for k, v in self._description_osm_map.items():
			if (lat >= v['minlat'] and lat <= v['maxlat'] and
				lon >= v['minlon'] and lon <= v['maxlon']):
				return k
		return None
