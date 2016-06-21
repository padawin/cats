# -*- coding: utf-8 -*-

import random

from src import actor


class simulator(object):
	MAX_TURNS = 100000
	STATE_CATS_MISSING = 0
	STATE_ALL_CATS_FOUND = 1

	def __init__(self, network, messenger=None, verbose=False):
		self.turn = 0
		self.verbose = verbose
		self.messenger = messenger
		self.network = network

	def initialiseActors(self, actorsNumber):
		positionActors = [
			# Takes 2 different values from the keys of the graph's nodes
			# each value will be the position of the cat and of the owner
			random.sample(self.network.getStationKeys(), 2)
			# this repeated as many times as we have actors
			for _ in range(actorsNumber)
		]

		# used for direct access to cats from human
		self.nodesHavingCats = {}
		# used to loop on the cats to update them
		self.cats = []
		self.humans = {}
		for actorId, stationIds in enumerate(positionActors):
			self.humans[actorId] = simulator._createHuman(
				actorId,
				stationIds[0],
				self.network
			)

			cat = simulator._createCat(actorId, stationIds[1])
			self.message(
				'cat located at {}',
				[self.network.getStationName(stationIds[1])],
				True
			)
			self._trackCatPosition(cat)
			self.cats.append(cat)

	@staticmethod
	def _createHuman(idHuman, stationId, network):
		human = actor.human(idHuman)
		human.setStationId(stationId)
		human.setNetwork(network)
		return human

	@staticmethod
	def _createCat(idCat, stationId):
		cat = actor.cat(idCat)
		cat.setStationId(stationId)
		return cat

	def _trackCatPosition(self, cat, oldPosition=None):
		if oldPosition is not None:
			self.nodesHavingCats[oldPosition].remove(cat)

		stationId = cat.stationId
		if stationId not in self.nodesHavingCats:
			self.nodesHavingCats[stationId] = []

		self.nodesHavingCats[stationId].append(cat)

	def _getNeighbourNodes(self, stationId):
		return self.network.getStationConnections(
			stationId
		)

	def _checkNodeForCats(self, human):
		'''
		If there is at least one cat where the human is, broadcast a message
		to the other humans to tell them a cat has been spotted in a given
		station.
		'''

		if human.stationId not in self.nodesHavingCats.keys():
			return

		cats = self.nodesHavingCats[human.stationId]
		for cat in cats:
			toContact = self.humans[cat.id]
			# The current human's cat is found
			if toContact is human:
				human.catRetrieved()
				self.cats.remove(cat)
				self.nodesHavingCats[human.stationId].remove(cat)
				self.network.closeStation(human.stationId)
				self.message(
					'Owner {} found cat {} - {} is now closed.',
					[
						human.id, cat.id,
						self.network.getStationName(human.stationId)
					]
				)
			# Another human's cat is found, notify the owner
			else:
				canReach = toContact.catFoundAt(human.stationId)
				if canReach:
					self.message(
						'{} saw cat {} at {}, heading there from {}',
						[
							human.id,
							toContact.id,
							self.network.getStationName(toContact.stationId),
							self.network.getStationName(human.stationId)
						],
						True
					)

	def step(self):
		if len(self.cats) == 0:
			return simulator.STATE_ALL_CATS_FOUND

		# Update the cats first
		for cat in self.cats:
			oldPosition = cat.stationId
			cat.update(self.turn, self._getNeighbourNodes(cat.stationId))
			# If the cat moved, track him
			if cat.stationId != oldPosition:
				self._trackCatPosition(cat, oldPosition)

		nbRemainingHumans = 0
		for idHuman in self.humans:
			human = self.humans[idHuman]
			# Check to know if any cats arrived at the human's station
			self._checkNodeForCats(human)
			# update each human with the current turn and the neighbour nodes, he
			# can access
			human.update(self.turn, self._getNeighbourNodes(human.stationId))
			# Check to know if there are any cats where the human arrived
			self._checkNodeForCats(human)
			if human.isLookingForCat():
				nbRemainingHumans += 1

		# Update turn number
		self.turn += 1

		if nbRemainingHumans == 0:
			return simulator.STATE_ALL_CATS_FOUND

		return simulator.STATE_CATS_MISSING

	def mainLoop(self):
		result = simulator.STATE_CATS_MISSING
		while len(self.cats) > 0 and self.turn < simulator.MAX_TURNS\
			and result == simulator.STATE_CATS_MISSING:
			result = self.step()

		self._sendReport()

	def _sendReport(self):
		totalHumanTurns = 0
		for h in self.humans:
			message = ''
			if self.humans[h].isLookingForCat():
				message = '{} is still looking'
				data = [h]
			else:
				message = '{} found cat in {} turns'
				data = [h, self.humans[h].nbStationsVisited]
			self.message(message, data, True)
			totalHumanTurns += self.humans[h].nbStationsVisited

		self.message(
			'Simulation finished after {} turns', [self.turn],
			True
		)
		self.message('Total number of cats: {}', [len(self.humans)])
		self.message(
			'Number of cats found: {}',
			[len(self.humans) - len(self.cats)]
		)
		self.message(
			'Average number of movements required to find a cat: {}',
			[totalHumanTurns / len(self.humans)]
		)

	def message(self, message, data=None, onlyVerbose=False):
		isVerboseLevelOk = self.verbose and onlyVerbose or not onlyVerbose
		if data:
			message = message.format(*data)

		if isVerboseLevelOk and self.messenger is not None:
			self.messenger.print(message)