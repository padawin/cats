# -*- coding: utf-8 -*-
class network(object):
	'''
	This class is a graph representation of the underground network.
	It has a list of stations (nodes). each station has a list of connections
	(edges).

	if the station 1 has in its connections the station 42, then the station
	42 will have the station 1 in its connections (non oriented graph)
	'''

	STATION_CLOSED = 0
	STATION_OPEN = 1

	def __init__(self, nodes, connections):
		'''
		Construct. Build the nodes graph
		'''

		if type(nodes) is not list:
			raise ValueError('The nodes argument must be a list')

		if type(connections) is not list:
			raise ValueError('The connections argument must be a list')

		self.nodes = {
			station[0]: {
				'name': station[1],
				'status': network.STATION_OPEN,
				'connections': [],
				'closedConnections': []
			}
			for station in nodes
		}

		for connection in connections:
			station1 = connection[0]
			station2 = connection[1]
			self.nodes[station1]['connections'].append(station2)
			self.nodes[station2]['connections'].append(station1)

	def closeStation(self, stationId):
		stationId = self.formatStationKey(stationId)
		if self.nodes[stationId]['status'] == network.STATION_CLOSED:
			return

		self.nodes[stationId]['status'] = network.STATION_CLOSED
		for station in self.nodes[stationId]['connections']:
			self.nodes[station]['connections'].remove(stationId)
			self.nodes[station]['closedConnections'].append(stationId)

	def getStationName(self, stationId):
		stationId = self.formatStationKey(stationId)
		return self.nodes[stationId]['name']

	def getStationConnections(self, stationId):
		stationId = self.formatStationKey(stationId)
		return self.nodes[stationId]['connections']

	def formatStationKey(self, stationKey):
		stationKey = str(stationKey)

		if stationKey not in self.nodes:
			raise ValueError('Invalid station "{}"'.format(stationKey))

		return stationKey
