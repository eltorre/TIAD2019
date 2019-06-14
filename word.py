#! /usr/bin/python3

class Word: 
	""" Holds information for a word"""
	def __init__(self, surface, cat, lang):
		self.surface = surface
		self.cat = cat
		self.lang = lang

	def __str__(self):
		return self.surface + "|" + self.cat +  "|" + self.lang
		
	def __eq__(self, other):
		return self.__dict__ == other.__dict__

class WordPair:
	""" Holds a pair of words. WordPair(x,y) == WordPair(y,x) """
	def __init__(self, word1, word2):
		if (word1.lang > word2.lang):
			self.pair = (word1, word2)
		else:
			self.pair = (word2, word1)
			
	def __eq__ (self, other):
		#Touple comparison is made element by element; if all are equal, it returns true.
		return self.pair == other.pair
		
	def getStrPair(self):
		return (str(self.pair[0]),str(self.pair[1]))
		
	def __str__(self):
		return str(self.pair[0]) + "-" + str(self.pair[1])
