class network(object):
	def __init__(self, stations):
		'''
		Construct. Build the stations graph
		'''

		self.stations = {
			station[0]: {'name': station[1], 'connections': []} for station in stations
		}
