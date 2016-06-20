class actor(object):
	def __init__(self):
		self.stationId = None

	def setStationId(self, stationId):
		self.stationId = stationId


class cat(actor):
	pass


class human(actor):
	def __init__(self):
		super().__init__()
		self.lastVisitedStation = None

	def setStationId(self, stationId):
		self.lastVisitedStation = self.stationId
		super().setStationId(stationId)
