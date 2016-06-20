import random


class actor(object):
	def __init__(self):
		self.stationId = None

	def setStationId(self, stationId):
		self.stationId = stationId

	def chooseStationId(self, stationIds):
		raise NotImplementedError(
			'I am a soulless actor, I cannot choose a station'
		)


class cat(actor):
	def chooseStationId(self, stationIds):
		if len(stationIds):
			self.setStationId(random.choice(stationIds))


class human(actor):
	def __init__(self):
		super().__init__()
		self.lastVisitedStation = None
		self.hasFoundCat = False

	def setStationId(self, stationId):
		self.lastVisitedStation = self.stationId
		super().setStationId(stationId)

	def chooseStationId(self, stationIds):
		candidates = [
			stationId
			for stationId in stationIds
			if stationId != self.lastVisitedStation
		]

		if candidates == []:
			candidates = stationIds

		if len(candidates):
			self.setStationId(random.choice(candidates))
