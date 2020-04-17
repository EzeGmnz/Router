from xml.dom import minidom

''' administrative class for the osm files serving as database'''
class database:

	''' files: file name list'''
	def __init__(self, files = None):
		if files is None:
			self._file_list = []
		else:
			self._file_list = files
		pass

	''' add a file to existing ones
	file: the file to add '''
	def addFile(self, file):
		self._file_list.append(file)
		pass

	# Returns the osm description
	# file minidom xml file
	def _getFileDescription(xml):
		output_map = {}
		
		# retrieving bounds
		bounds = xml.getElementsByTagName('bounds')
		output_map['minlat'] = bounds.getAttribute('minlat')
		output_map['minlon'] = bounds.getAttribute('minlon')
		output_map['maxlat'] = bounds.getAttribute('maxlat')
		output_map['maxlon'] = bounds.getAttribute('maxlon')

		# retrieving name
		nodes = xml.getElementsByTagName('node')
		for n in nodes:
			tags = nodes.getElementsByTagName('tag')
			name = None
			place = None
			i = 0
			while i < len(tags) and name is None and place is None:
				t = tags[i]
				if t.getAttribute('k') == 'name'
					name = t.getAttribute('v')
				elif t.getAttribute('v') == 'place'
					place = t.getAttribute('v')
				i += 1
		 	if final_node is not None:
		 		output_map['name'] = name
		 		break
		return output_map

	''' Return the osm file corresponding to the coordinate, if exists, otherwise return None'''
	def getSection(self, coordinate):
		section = None
		lat, lon = coordinate
		for x in _file_list:
			xml = minidom.parse(x)
			
			# Checking if coordinate lands in the osm file bounds
			current_file_desc = -_getFileDescription(xml)
			if lat >= output_map['minlat'] and lat <= output_map['maxlat'] and
				lon >= output_map['minlon'] and lon <= output_map['maxlon']:
				return x
		return None