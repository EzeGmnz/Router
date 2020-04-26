#!/usr/bin/env python
"""
Goeocoder Interface
"""

__author__ = "Ezequiel Giménez"
__copyright__ = "Copyright 2020, Router project"
__credits__ = ["Ezequiel Giménez"]
__maintainer__ = "Ezequiel Giménez"
__email__ = "eze.gimenez.98@gmail.com"
__status__ = "Development"

class IGeocoder:

	def geocode(self, address):
		raise NotImplementedError