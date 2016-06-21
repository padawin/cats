# -*- coding: utf-8 -*-
import random
from src import ai

'''
Module to manage the simulation's actors.
The actors are the cats and humans. Each have a dedicated class, both
inheriting the actor class.
'''


class actor(object):
	'''
	An actor has an id and a station ID (as position).
	Also the actor offers the possibility to choose a station ID from a list
	but leaves the implementation to the child (as abstract as a method can be
	in python)
	'''

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
		'''
		If the station ids list is not empty, a cat just randomly pick one in
		the list.
		'''

		if len(stationIds):
			self.setStationId(random.choice(stationIds))
			return True

		return False

	def update(self, turn, neighbourStations):
		'''
		cats have their time, they move slowly, so they will change
		station only one turn out of 2
		'''
		if (turn % 2) == 1:
			self.chooseStationId(neighbourStations)


class human(actor):
	'''
	A human has different states depending on the search of its cat:
	STATE_LOOKS_FOR_CAT: the human is looking for its cat. If self.targetStation
		is None, it just roams around, hoping to find its cat, if
		self.targetStation is not None, the human is walking towards this
		station (being the station where the cat has been last spotted)
	STATE_FOUND_CAT: the human found its cat and they are happy together,
		roaming the network
	STATE_CANNOT_REACH_CAT: the human received the position of its cat, but
		can't reach it (the only way being via a closed station). In this case,
		the human still roams around to notify the owners of any cat which will
		pass in the same station as him

	The human has a brain attribute being a pathFinder instance, used to find
	paths to reach the cat.

	The human can have access to the network graph (just like a map) to find its
	way.
	'''

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
		'''
		At each change of station, save the previously visited station to not
		be able to alternate between two stations when roaming around.
		'''
		# @TODO could be improved with a list of last visited stations
		self.lastVisitedStation = self.stationId
		super().setStationId(stationId)

	def chooseStationId(self, stationIds):
		'''
		If no station Ids are provided, returns False.

		stationIds is meant to be a list.

		The last visited station is excluded from the provided list. If after that
		the candidates is an empty list, take the original list, to go to the
		previously visited station.
		'''
		if len(stationIds) == 0:
			return False

		candidates = [
			stationId
			for stationId in stationIds
			if stationId != self.lastVisitedStation
		]

		if candidates == []:
			candidates = stationIds

		self.setStationId(random.choice(candidates))
		if not self.hasFoundCat():
			self.nbStationsVisited += 1

		return True

	# States tests
	def isLookingForCat(self):
		return not self.hasLastPosition() and self.state == human.STATE_LOOKS_FOR_CAT

	def hasLastPosition(self):
		return self.targetStation is not None

	def hasFoundCat(self):
		return self.state == human.STATE_FOUND_CAT

	def cantReachCat(self):
		return self.state == human.STATE_CANNOT_REACH_CAT

	def catRetrieved(self):
		self.state = human.STATE_FOUND_CAT
	# End of states tests

	def update(self, neighbourStations):
		'''
		Method to update the human's position
		Gets a list of neighbour stations to its current station.
		If the human knows where its cat has been spotted, it will ignore the
		stations list and will figure out if there is a path to go to the cat's
		last known position.
		If there is no path, it will enter the state of STATE_CANNOT_REACH_CAT
		and will pick a random station to go to.
		'''

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
		'''
		Method called when a human's cat is spotted. The stationId provided is
		the station where the cat has been spotted. If the human already knows
		it can't reach the cat, nothing will be done, otherwise, the target
		station will be set.
		'''

		# It is not important for the human anymore to know where the
		# cat is. He used to be able to reach it but a station closed in
		# the meantime
		if self.cantReachCat():
			return False

		self.targetStation = stationId
		return True
