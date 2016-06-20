# -*- coding: utf-8 -*-
import random


class actor(object):
	def __init__(self, idActor):
		self.id = idActor
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
			return True

		return False

	def update(self, turn, neighbourStations):
		# cats have their time, they move slowly, so they will change
		# station only one turn out of 2
		if (turn % 2) == 1:
			self.chooseStationId(neighbourStations)


class human(actor):
	STATE_LOOKS_FOR_CAT = 1
	STATE_GOES_TO_LAST_KNOWN_POSITION = 2
	STATE_FOUND_CAT = 3

	def __init__(self, idHuman):
		super().__init__(idHuman)
		self.lastVisitedStation = None
		self.targetStation = None
		self.state = human.STATE_LOOKS_FOR_CAT

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
			return True

		return False

	def isItMyCat(self, catId):
		return catId == self.id

	def isLookingForCat(self):
		return self.state == human.STATE_LOOKS_FOR_CAT

	def update(self, turn, neighbourStations):
		if self.isLookingForCat():
			self.chooseStationId(neighbourStations)

	def catFoundAt(self, stationId):
		self.targetStation = stationId
		self.state = human.STATE_GOES_TO_LAST_KNOWN_POSITION

	def catRetrieved(self):
		self.state = human.STATE_FOUND_CAT
