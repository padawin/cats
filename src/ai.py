# -*- coding: utf-8 -*-


class pathFinder(object):
	def findPath(self, grid, startNode, endNode):
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
		path = []
		while toNode is not None:
			path.append(toNode['id'])
			toNode = toNode['previous']
		return path

	def _chooseNode(self, reachables):
		bestNode = None
		for node in reachables:
			if bestNode is None or bestNode['cost'] > reachables[node]['cost']:
				bestNode = reachables[node]
		return bestNode
