class actor(object):
	def __init__(self):
		self.stationId = None

	def setStationId(self, stationId):
		self.stationId = stationId


class cat(actor):
	pass


class human(actor):
	pass
