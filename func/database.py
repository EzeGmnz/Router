#!/usr/bin/env python
"""
Osm file managment and administration
"""
from xml.dom import minidom
from .utils import nameComparison
import time

__author__ = "Ezequiel Giménez"
__copyright__ = "Copyright 2020, Router project"
__credits__ = ["Ezequiel Giménez"]
__maintainer__ = "Ezequiel Giménez"
__email__ = "eze.gimenez.98@gmail.com"
__status__ = "Development"

''' Osm files accesing is done from here'''
class Database:

	class Vividict(dict):
		def __getitem__(self, item):
			try:
				return dict.__getitem__(self, item)
			except KeyError:
				value = self[item] = type(self)()
				return value

	''' files: file name list'''
	def __init__(self, files = None):
		if files is None:
			self._file_list = []
		else:
			self._file_list = files
		
		self._parsed_files = {}
		self._osm_description = {}

		for file in self._file_list:
			self._osm_description[file] = self._getFileDescription(minidom.parse(file))
			self._parsed_files[file] = self.getFileParsed(file)

	''' Add a file to existing ones
	file: the file to add '''
	def addFile(self, file):
		if file not in self._file_list:
			self._file_list.append(file)
			self._osm_description[file] = self._getFileDescription(minidom.parse(file))
			self._parsed_files[file] = self.getFileParsed(file)
		pass

	def _getNameAndNumberFromNode(self, node):
		tags = node.getElementsByTagName('tag')

		street, number = None, None
		i = 0
		while i < len(tags) and (street is None or number is None):
			if 'addr:street' == tags[i].getAttribute('k'):
				street = tags[i].getAttribute('v')
			elif 'addr:housenumber' == tags[i].getAttribute('k'):
				number = int(float(tags[i].getAttribute('v').split(' ')[0]))
			i += 1

		return street, number

	# adds to map the parsed .osm xml document
	def getFileParsed(self, file):


		###TODO
		start = time.perf_counter()
		print("START\tgetFileParsed ", time.perf_counter())
		###


		xml = minidom.parse(file)
		nodes = xml.getElementsByTagName('node')
		output_map = self.Vividict()
		for n in nodes:
			street, number = self._getNameAndNumberFromNode(n)
			if street is not None and number is not None:
				output_map[street][number] = (float(n.getAttribute('lat')), float(n.getAttribute('lon')))
		
		###
		end = time.perf_counter()
		print("END\tgetFileParsed", time.perf_counter(), " - " , end-start)
		###

		return output_map

	# returns file parse
	def get(self, file):
		if file in self._parsed_files.keys():
			return self._parsed_files[file]
		return None

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
		for k, v in self._osm_description.items():
			for x in address.split(","):
				if nameComparison(v['name'], x):
					return k
		return None

	''' Return the first osm file holding the coordinate, if exists, otherwise return None'''
	def getSectionFromCoordinate(self, coordinate):
		lat, lon = coordinate
		for k, v in self._osm_description.items():
			if (lat >= v['minlat'] and lat <= v['maxlat'] and
				lon >= v['minlon'] and lon <= v['maxlon']):
				return k
		return None