"""
Author: Kevin Holligan
CSCI 5454 Algorithms
Karger Min Cut and Karger-Stein
2016
"""

import math
import random
import copy
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os

#Generate a random graph from the Erdos-Renyi model
def createRandomGraph(size, p):
	graph = nx.fast_gnp_random_graph(size, p)
	#Make sure our graph is connected
	while not nx.is_connected(graph):
		graph = nx.fast_gnp_random_graph(size,p)
	return graph

#To combine to a pair of nodes (u,v) into single node u,
#take the edges from node v and add them to node u, then delete node v
def contractEdges(graph, node, node2):

	for e in graph.edges(node2):
		#Make sure we're not adding self loops
		if e[1] is not node:
			graph.add_edge(node,e[1])
	graph.remove_node(node2)

	return graph

#Helper function to iterate through generated graph and print edges (u,v)
def printGraph(graph):
	for n,nbrs in graph.adjacency_iter():
		for nbr,eattr in nbrs.items():
			print('(%d, %d)' % (n,nbr))

#Pick a random edge, contract it. Repeat until only two nodes remaining
def kargerMinCut(graph, remainingNodes):
	while graph.number_of_nodes()>remainingNodes:
		u,v = random.choice(graph.edges())
		graph = contractEdges(graph, u,v)
	return graph

def minCut(graph):

	gprime = nx.MultiGraph()
	gprime.add_nodes_from(graph)
	gprime.add_edges_from(graph.edges())

	while gprime.number_of_nodes() > 2:
		for n, nbrs in gprime.adjacency_iter():
			contractEdges(gprime)

def kargerSteinMinCut(graph, vertices):
	nodes = graph.number_of_nodes()

	if nodes >= 6:
		vertices = (1 + nodes/math.sqrt(2))
		G1 = kargerMinCut(graph, vertices)
		G2 = kargerMinCut(graph, vertices)

		return min(kargerSteinMinCut(G1, 0), kargerSteinMinCut(G2,0))
	else:
		cutSize = 0
		edgeSet = nx.minimum_edge_cut(graph)
		#Find the edges in the nodes in the edge set and add them up to get cut size
		for n in edgeSet:
			cutSize += graph.number_of_edges(n[0],n[1])
		return cutSize


def createBoxplot(graphSizes, probabilityList):
	
	data = []
	# Extract data
	for n in graphSizes:
		data.append(probabilityList[n])

	#Make boxplot
	plt.figure()
	plt.boxplot(data)
	plt.title("Distribution of successfully selecting min cut")
	plt.xticks(np.arange(7),('','2','3','5','8','13','21'))
	plt.yticks(np.arange(0.00,1.01,0.1))
	plt.xlabel("Nodes in graph")
	plt.ylabel("Percent success")
	plt.show()

if __name__ == "__main__":
	p = 0.5
	
	repetitions = 30
	sizeOfGraphs = [2,3,5,8,13,21]
	probability = dict()
	mode = 1 # 0 for Karger, 1 for Karger-Stein

	for n in sizeOfGraphs:
		
		for i in range(repetitions):
			graph = createRandomGraph(n, p)
			# printGraph(graph)

			#Initialize min cut and first iteration cut to infinite
			minCut = float("inf")
			monteCarloAttempts = 10*21*21
			cutSuccess = 0.0
			listOfAttempts = []

			# Find the minimum cut
			# Record the size of the cut from the first attempt
			for j in range(monteCarloAttempts):
				# create a new copy of the graph
				# use a multi graph so that we can have parallel edges between nodes
				gprime = nx.MultiGraph()
				gprime.add_nodes_from(graph)
				gprime.add_edges_from(graph.edges())

				# Use Karger or Karger-Stein
				switch(mode):
					case 0:
						gprime = kargerMinCut(gprime,2)
						cutSize = gprime.number_of_edges()
						break
					case 1:
						cutSize = kargerSteinMinCut(gprime,0)
						break

				if cutSize < minCut:
					minCut = cutSize
				listOfAttempts.append(cutSize) #record our cut results

			# Count up the number of times we got the min number of cuts
			for cuts in listOfAttempts:
				if cuts is minCut:
					cutSuccess += 1

			# Add the number of nodes, probability of success to the dict
			if n in probability:
				probability[n].append(float(cutSuccess/monteCarloAttempts))
			else:
				probability[n] = [float(cutSuccess/monteCarloAttempts)]	
			#Print it so that you know something is happening		
			print("Nodes: %.0f, minCut: %.0f, successes: %.0f, attempts: %.0f, prob: %0.3f" % (n, minCut, cutSuccess, monteCarloAttempts, float(cutSuccess/monteCarloAttempts)))

	createBoxplot(sizeOfGraphs, probability)
