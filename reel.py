#! /usr/bin/python3

import sys
import concurrent.futures
from igraph import *
from word import Word, WordPair
import argparse

def processTree(tree, newWord, newWords, newestWords, oldWords, toRet):
	for pair in tree.reel(newWord):
		if pair not in toRet and newWord.cat:
			toRet.append(pair)
		for w in pair.pair:
			if w not in oldWords and w not in newWords and w not in newestWords:
				newestWords.append(w)	

def reel(trees, word,  depth, workers):
	toRet = []
	oldWords = []
	newWords = [word]
	
	while depth > 0 and newWords:
		# ~ print("Epochs left:", depth, " New nodes found:", len(newWords))
		newestWords = []
		with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
			futures = [executor.submit(processTree, tree, newWord, newWords, newestWords, oldWords, toRet) for newWord in newWords for tree in trees ]
			concurrent.futures.wait(futures)
#		print ("NEWEST ", " ".join(str(x) for x in newestWords))
#		print ("NEW ", " ".join(str(x) for x in newWords))
#		print ("OLD ", " ".join(str(x) for x in oldWords))
		oldWords = oldWords + newWords
		newWords = newestWords
		depth -= 1

	return toRet

parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument("-w", "--word", dest="word", help="The seed word", required=True, metavar="word")
requiredNamed.add_argument("-l", "--lang", dest="lang", help="Language of the seed word", required=True, metavar="lang")
requiredNamed.add_argument("-f", "--dictionary", dest="triplets", help="Triplets with (source lang, target lang, file)", required=True, nargs="+", metavar=["source lang","target lang","apertium bidix"], action='append')

optional = parser.add_argument_group('optional arguments')
optional.add_argument("-d", "--depth", dest="depth", help="Maximum depth in the search", default=5, type=int, metavar="depth")
optional.add_argument("-o", "--outputmode", dest="outputmode", help="Output mode", default="stdout", choices=["stdout", "graph", "d3js"])
optional.add_argument("-j", "--workers", dest="workers", help="Maximum number of threads/processes", default=4, type=int, metavar="workers")
optional.add_argument("-c", "--colours", dest="colours", help="Pairs with (lang, color)", nargs=2, metavar=["lang", "colour"], action='append')
optional.add_argument("-s", "--size", dest="size", help="Size of the graph (x, y)", nargs=2, type=int, metavar=["x size","y size"])
optional.add_argument('-m', "--memory", dest="memory", help="Stores the dictionaries in a trie to speed up search (and slow down the start up time)", action="store_true")


args = parser.parse_args()
workers = args.workers
word = Word(args.word, "", args.lang)
depth = args.depth

if args.memory:
	from apertiumBidictMemory import ApertiumBidict
else:
	from apertiumBidict import ApertiumBidict

if args.colours:
	colour_dict = {}
	for colour in args.colours:
		colour_dict[colour[0]] = colour[1]
else:
	colour_dict = {"es": "blue", "fr": "pink", "en":"green", "pt":"black"}

if args.size:
	size = (args.size[0],args.size[1])
else:
	size = (1920, 1080)

trees = []
futures = []
with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
	for triplet in args.triplets:
		futures.append(executor.submit(ApertiumBidict, *triplet))
concurrent.futures.wait(futures)
for future in futures:
	trees.append(future.result())


edges = reel(trees, word, depth, workers)
edges = list(set((x.getStrPair() for x in edges)))

if args.outputmode == "graph":
	nodes = []
	for edge in edges:
		nodes.append(edge[0])
		nodes.append(edge[1])
	nodes = list(set(str(x) for x in nodes))
	G = Graph()
	G.add_vertices(nodes)
	G.add_edges(edges)
	G.vs["label"] = G.vs["name"]
	G.vs["color"] = [colour_dict[x.split("|")[2]] for x in G.vs["name"]]
	layout = G.layout_kamada_kawai	()
	plot(G, layout=layout, margin=100, bbox=size, vertex_label_dist = 1)
elif args.outputmode == "d3js":
	import json
	edgesJs = []
	nodes = []
	nodeNames = []
	for edge in edges:
		for vertex in edge:
			(surf,pos,lang) = vertex.split("|")
			if vertex not in nodeNames:
				nodes.append({"group":lang+"_"+pos, "id":vertex})
				nodeNames.append(vertex)
		v1 = edge[0]
		v2 = edge[1]
		edgesJs.append({"source":v1, "target":v2})
	print(json.dumps({"links":edgesJs, "nodes":nodes}))
else:
	print(edges)
