# -*- coding: utf-8 -*-
import random
import ai


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
	STATE_FOUND_CAT = 2
	STATE_CANNOT_REACH_CAT = 3

	def __init__(self, idHuman):
		super().__init__(idHuman)
		self.nbStationsVisited = 0
		self.lastVisitedStation = None
		self.targetStation = None
		self.state = human.STATE_LOOKS_FOR_CAT
		self.network = None
		self.brain = ai.pathFinder()

	def setNetwork(self, network):
		self.network = network

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
			if not self.hasFoundCat():
				self.nbStationsVisited += 1
			return True

		return False

	def isItMyCat(self, catId):
		return catId == self.id

	def isLookingForCat(self):
		return not self.hasLastPosition() and self.state == human.STATE_LOOKS_FOR_CAT

	def hasLastPosition(self):
		return self.targetStation is not None

	def hasFoundCat(self):
		return self.state == human.STATE_FOUND_CAT

	def cantReachCat(self):
		return self.state == human.STATE_CANNOT_REACH_CAT

	def update(self, turn, neighbourStations):
		if self.hasLastPosition():
			# the human knows where the cat was at some point, so
			# he will try to head towards this position.
			# The path must be recalculated each time because potentially
			# a station on the way closed and broke it
			path = self.brain.findPath(self.network, self.stationId, self.targetStation)
			if path == []:
				# A station closed and made it impossible for the human to
				# reach its cat
				self.targetStation = None
				self.state = human.STATE_CANNOT_REACH_CAT
			else:
				# The path is calculated, get the first step
				self.setStationId(path[0])
				if len(path) == 1:
					self.targetStation = None
				# We have the next station to go to, we are done here
				return

		self.chooseStationId(neighbourStations)

	def catFoundAt(self, stationId):
		# It is not important for the human anymore to know where the
		# cat is. He used to be able to reach it but a station closed in
		# the meantime
		if self.cantReachCat():
			return False

		self.targetStation = stationId
		return True

	def catRetrieved(self):
		self.state = human.STATE_FOUND_CAT
