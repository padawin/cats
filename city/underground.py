class network(object):
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
