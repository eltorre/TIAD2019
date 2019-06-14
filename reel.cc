#include <iostream>
#include <string>
#include <cstring>
#include <stdio.h>
#include <list>
#include <vector>
#include <algorithm>
#include <thread>

using namespace std;

// Graph class represents a directed graph
// using adjacency list representation
class Graph
{
	private:
		int V;	// No. of vertices
		// Pointer to an array containing
		// adjacency lists
		vector< list<int> > adj;
		// A recursive function used by DFS
		void DFSUtil(int v, bool visited[]);
	public:
		Graph();   // Constructor
		// function to add an edge to graph
		void addEdge(int v, int w);
		// DFS traversal of the vertices
		// reachable from v
		void DFS(bool marked[], int curLength, int vert, int start, int path[], int maxLength);
		void printCycles(int maxLength);
		vector<string> *vocab;
};

Graph::Graph()
{

}

void Graph::addEdge(int v, int w)
{
	if (adj.size() < v+1){
		adj.resize(v+1);
	}
	if (adj.size() < w+1){
		adj.resize(w+1);
	}
	adj[v].push_back(w); // Add w to v’s list.
	adj[w].push_back(v); // Add w to v’s list.
	V = adj.size();
}

void Graph::DFS(bool marked[], int curLength, int vert, int start, int path[], int maxLength)
{
	// mark the vertex vert as visited
	marked[vert] = true;

	// if the path of length (n-1) is found
	if (curLength == 0) {

		// mark vert as un-visited to make
		// it usable again.
		marked[vert] = false;

		// Check if vertex vert can end with
		// vertex start
		if (find(adj[vert].begin(), adj[vert].end(), start) != adj[vert].end())
		{
			string toPrint = vocab->at(start);
			for (int i = 0; i < maxLength-1; i++){
				toPrint += " " + vocab->at(path[i]);
			}
			cout <<toPrint <<endl;
			return;
		} else
			return;
	}

	for (list<int>::iterator it = adj[vert].begin(); it != adj[vert].end(); it++) {
		if (!marked[*it]) {
			//~ cerr<< "Checking " <<curLength <<" " <<vert <<" to " <<*it <<" " <<start << endl;
			path[curLength-1] = *it;
			DFS(marked, curLength-1, *it, start, path, maxLength);
		}
	}

	// marking vert as unvisited to make it
	// usable again.
	marked[vert] = false;
}

// Counts cycles of length N in an undirected
// and connected graph.
void Graph::printCycles(int maxLength)
{
	cerr << "Total nodes " <<V <<endl;
	// all vertex are marked un-visited intially.
	bool marked[V];
	int path[maxLength-1];
	memset(marked, 0, sizeof(marked));
	
	// Searching for cycle by using v-n+1 vertices
	int count = 0;
	for (int i = 0; i < V - (maxLength - 1); i++) {
		cerr << "Processing " <<vocab->at(i) << " " <<i << ":" <<V << endl;
		DFS(marked, maxLength-1, i, i, path, maxLength);

		// ith vertex is marked as visited and
		// will not be visited again.
		marked[i] = true;
	}
}

int main(int argv, char** argc) {
	string input_line, lword, rword;
	int lindex, rindex;
	vector<string>::iterator lit, rit;
	int tabPos=0;
	vector<string> vocab;
	Graph graph;

	while (std::getline(std::cin, input_line)) {
		tabPos = input_line.find("\t");
		lword = input_line.substr(0, tabPos);
		rword = input_line.substr(tabPos+1, input_line.length());

		lit = find (vocab.begin(), vocab.end(), lword);
		if (lit == vocab.end()){
			vocab.push_back(lword);
			lit = vocab.end();
			--lit;
		}
		lindex = distance(vocab.begin(), lit);
		rit = find (vocab.begin(), vocab.end(), rword);
		if (rit == vocab.end()){
			vocab.push_back(rword);
			rit = vocab.end();
			--rit;
		}
		rindex = distance(vocab.begin(), rit);
		//~ 	  ., HBcerr << "Adding edge " << lindex << "(" << vocab[lindex] <<") " <<rindex  << "(" << vocab[rindex] <<") " << endl;
		graph.addEdge(lindex, rindex);
	}
	
	graph.vocab = &vocab;
	
	graph.printCycles(4);
}
