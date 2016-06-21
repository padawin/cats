# -*- coding: utf-8 -*-

'''
Module to manage the actors' AI. Handles only the humans' path finding at the
moment.
'''


class pathFinder(object):
	def findPath(self, grid, startNode, endNode):
		'''
		Method to find a path between startNode and endNode. If no path exists,
		[] is returned.
		'''

		reachables = {startNode: {'id': startNode, 'previous': None, 'cost': 0}}
		visited = []
		visitedIds = []

		while reachables != {}:
			node = self._chooseNode(reachables)
			if node['id'] == endNode:
				return self._buildPath(node)

			del reachables[node['id']]
			visited.append(node)
			visitedIds.append(node['id'])

			for adjacent in grid.getStationConnections(node['id']):
				if adjacent not in visitedIds:
					if adjacent not in reachables:
						adjacentNode = {'id': adjacent, 'previous': node, 'cost': float('inf')}
						reachables[adjacent] = adjacentNode
					else:
						adjacentNode = reachables[adjacent]

					if node['cost'] + 1 < adjacentNode['cost']:
						adjacentNode['previous'] = node
						adjacentNode['cost'] = node['cost'] + 1

		return []

	def _buildPath(self, toNode):
		'''
		Build the path to go to toNode, by using the chain of previouses
		'''

		path = []
		while toNode is not None:
			path.append(toNode['id'])
			toNode = toNode['previous']

		# path goes from end (included) to start (included), it has to be
		# reversed and start must be excluded
		return path[-2::-1]

	def _chooseNode(self, reachables):
		'''
		Method to choose a node among the reachables. Just checks on the cost to
		calculated so far.
		'''

		bestNode = None
		for node in reachables:
			if bestNode is None or bestNode['cost'] > reachables[node]['cost']:
				bestNode = reachables[node]
		return bestNode
