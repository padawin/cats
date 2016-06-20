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


class human(actor):
	STATE_LOOKS_FOR_CAT = 1
	STATE_GOES_TO_LAST_KNOWN_POSITION = 2
	STATE_FOUND_CAT = 3

	def __init__(self, idHuman):
		super().__init__(idHuman)
		self.lastVisitedStation = None
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

	def isItMyCat(self, catId):
		return catId == self.id
