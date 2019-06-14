#! /usr/bin/python3

#A trie
class Fixtree:
	"""A trie"""
	def __init__(self):
		self.data = []
		self.children = {}
	
	#Add data to the trie
	def addData(self, fix, datum):
		node = root = self
		while fix:
			if fix[0] not in node.children:
				node.children[fix[0]] = Fixtree()
			node = node.children[fix[0]]
			fix = fix[1:]
		node.data.append(datum)
	
	#Returns the list of nodes traversed with the given prefix, until is no longer possible to navigate
	def getFixStack(self, fix):
		toRet = [("", self)]
		node = self
		while fix:
			if fix[0] in node.children:
				node = node.children[fix[0]]
				toRet.append((fix[0], node))
				fix = fix[1:]
			else:
				return toRet #Not possible to navigate further
		return toRet
	
	#Returns the node corresponding to the given prefix, if it exists
	def getFix(self, fix):
		node = self
		while fix:
			if fix[0] in node.children:
				node = node.children[fix[0]]
				fix = fix[1:]
			else:
				return []
		return node.data
	
	#Dumps the tree as text (for debugging purposes)
	def dump(self, tab):
		if (self.data):
			 print (tab + " " + ",".join(self.data))
		for k,v in self.children.items():
			v.dump(tab+k)
