#!/usr/bin/env python
"""
Main coordinator
"""
import numpy as np
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from .retrieve import *
from .database import *
from .pathoptimizer import *
import time

__author__ = "Ezequiel Giménez"
__copyright__ = "Copyright 2020, Router project"
__credits__ = ["Ezequiel Giménez"]
__maintainer__ = "Ezequiel Giménez"
__email__ = "eze.gimenez.98@gmail.com"
__status__ = "Development"

class Router:

	def __init__(self):

		

	def getRouteFromAddresses(self, addresses):
