

import xml.etree.ElementTree as ET
from word import Word, WordPair
from trie import Fixtree

class ApertiumBidict:
	""" A class that looks for the corresponding pair of a given word by building a TRIE out of an Apertium dictionary"""
	def __init__(self, sLang, tLang, fileName):
		self.sLang = sLang
		self.tLang = tLang
		self.sTree = Fixtree()
		self.tTree = Fixtree()
		for node in ET.parse(fileName).iterfind(".//p"):
			sWord = ApertiumBidict.processNode(node.find("l"), sLang)
			tWord = ApertiumBidict.processNode(node.find("r"), tLang)
			self.sTree.addData(sWord.surface, tWord)
			self.tTree.addData(tWord.surface, sWord)
		for node in ET.parse(fileName).iterfind(".//i"):
			sWord = ApertiumBidict.processNode(node, sLang)
			tWord = ApertiumBidict.processNode(node, tLang)
			self.sTree.addData(sWord.surface, tWord)
			self.tTree.addData(tWord.surface, sWord)
			
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
			toRet += (WordPair(word, x) for x in self.sTree.getFix(word.surface))
		elif self.tLang == word.lang:
			toRet += (WordPair(word, x) for x in self.tTree.getFix(word.surface))
		return toRet
		
	def __str__(self):
		return self.sLang + "|" + self.tLang
