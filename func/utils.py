#!/usr/bin/env python
''' 
Utils
'''

__author__ = "Ezequiel Giménez"
__copyright__ = "Copyright 2020, Router project"
__credits__ = ["Ezequiel Giménez"]
__maintainer__ = "Ezequiel Giménez"
__email__ = "eze.gimenez.98@gmail.com"
__status__ = "Development"

street_naming_database_path = 'D:/Eze/Programacion/Router/SimpleServer/sandbox/func/streetnamingdatabase.txt'

''' 
Returns True if two names are alike, False otherwise
adjustabel threshold to improve accuracy
Uses Damerau-Levenstein algorithm two find string distances
Will return True if a name is alike a word included inside the other
'''
def nameComparison(str1, str2, threshold=2):
	list1 = str1.replace(',', ' ').split(' ')
	list2 = str2.replace(',', ' ').split(' ')
	for word1 in list1:
		for word2 in list2:
			if _DamerauLevensteinDistance(word1, word2, threshold):
				return True
	return False

# will remove common street naming as 'Avenida'
# those words are stored in street_naming_database_path file
def formatAddress(address):
	output = address
	with open(street_naming_database_path) as file:
		line = file.readline()
		while line:
			if line.lower() in address:
				output.replace(line, '')
			line = file.readline()
	return output

def _DamerauLevensteinDistance(str1, str2, threshold=2):

	d=dict()
	for i in range(len(str1)+1):
		d[i]={}
		d[i][0]=i
	for i in range(len(str2)+1):
		d[0][i] = i
	for i in range(1, len(str1)+1):
		for j in range(1, len(str2)+1):
			d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))

	return d[len(str1)][len(str2)] <= threshold