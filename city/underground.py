class network(object):
	'''
	This class is a graph representation of the underground network.
	It has a list of stations (nodes). each station has a list of connections
	(edges).

	if the station 1 has in its connections the station 42, then the station
	42 will have the station 1 in its connections (non oriented graph)
	'''

	def __init__(self, stations, connections):
		'''
		Construct. Build the stations graph
		'''

		if type(stations) is not list:
			raise ValueError('The stations argument must be a list')

		if type(connections) is not list:
			raise ValueError('The connections argument must be a list')

		self.stations = {
			station[0]: {'name': station[1], 'connections': []} for station in stations
		}

		for connection in connections:
			station1 = connection[0]
			station2 = connection[1]
			self.stations[station1]['connections'].append(station2)
			self.stations[station2]['connections'].append(station1)
