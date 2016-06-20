class network(object):
	def __init__(self, stations):
		'''
		Construct. Build the stations graph
		'''

		if type(stations) is not list:
			raise ValueError('The stations argument must be a list')

		self.stations = {
			station[0]: {'name': station[1], 'connections': []} for station in stations
		}
