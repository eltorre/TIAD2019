#! /usr/bin/python3

import xml.etree.ElementTree as ET
from word import Word, WordPair

class ApertiumBidict:
	""" A class that looks for the corresponding pair of a given word by searching in an Apertium dictionary DOM"""
	def __init__(self, sLang, tLang, file):
		self.sLang = sLang
		self.tLang = tLang
		self.tree = ET.parse(file)
	
	@staticmethod
	def processNode(node, lang):
		nodecat = node.find(".//s")
		if nodecat is not None:
			nodecat = nodecat.get("n")
		else:
			nodecat = "None"
		nodetext = ApertiumBidict.nodeToString(node)
		return Word(nodetext, nodecat, lang)
		
	@staticmethod
	def nodeToString(node):
		return "<b/>".join(x.text if x.text else "" + x.tail if x.tail else "" for x in node.iter() if (x.text or x.tail))

	def reel(self, word):
		if self.sLang != word.lang and self.tLang != word.lang:
			return []
		if "<" in word.surface:
			return [] #Skip multiwords
		toRet = []
		if self.sLang == word.lang: 
			for node in self.tree.findall(".//p[l='" + word.surface + "']/r"):
				toRet.append(WordPair(word, ApertiumBidict.processNode(node, self.tLang)))
			for node in self.tree.findall(".//e[i='" + word.surface + "']/i"): #No good way to look directly in the text node...
				toRet.append(WordPair(word, ApertiumBidict.processNode(node, self.tLang)))
		elif self.tLang == word.lang:
			for node in self.tree.findall(".//p[r='" + word.surface + "']/l"):
				toRet.append(WordPair(word, ApertiumBidict.processNode(node, self.sLang)))
			for node in self.tree.findall(".//e[i='" + word.surface + "']/i"):
				toRet.append(WordPair(word, ApertiumBidict.processNode(node, self.sLang)))
		return toRet
		
	def __str__(self):
		return self.sLang + "|" + self.tLang
