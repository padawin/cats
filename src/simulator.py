# -*- coding: utf-8 -*-

import random

from src import actor
from src import config

'''
This modules manages a simulation instance. It creates the actors, handle the
main loop and send messages to the calling application.
'''


class simulator(object):

	# Simulation state
	STATE_CATS_MISSING = 0
	STATE_ALL_CATS_FOUND = 1

	def __init__(self, network, messenger=None, verbose=False):
		'''
		The network is the graph in which the actors will evolve.
		The messenger is an object which must implement a send method to send
			some messages to the application (which then could do things like
			printing them on stdout, send them in sockets, log them in a
			file...)
		The verbose option decides if every messages will be sent to the
		messenger or just critical ones.
		'''
		self.turn = 0
		self.verbose = verbose
		self.messenger = messenger
		self.network = network

	def initialiseActors(self, actorsNumber):
		'''
		This methods creates <actorsNumber> cats and <actorsNumber> humans. Each
		pair of cat/human is on two different nodes of the network, but two
		cats, two humans or a cat and a human (not its owner) can be in the same
		stations.
		'''

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
		'''
		All the remaining cats are stored in a cats list and in a dict with the
		following structure:
		stationId: list of cats in the station

		When a cat moves, this method updates its position in the dict of
		stations.
		'''

		if oldPosition is not None:
			self.nodesHavingCats[oldPosition].remove(cat)

		stationId = cat.stationId
		if stationId not in self.nodesHavingCats:
			self.nodesHavingCats[stationId] = []

		self.nodesHavingCats[stationId].append(cat)

	def _getNeighbourNodes(self, stationId):
		'''
		Wrapper method, to have a lighter code where used.
		'''
		return self.network.getStationConnections(
			stationId
		)

	def _checkNodeForCats(self, human):
		'''
		When a human arrives at a station, it checks if there are cats there.
		If the human find its cat, the cat is removed and the station closed.

		If there is at least one cat where the human is (not belonging to the
		human, a message is broadcasted to the other humans to tell them a cat
		has been spotted in a given station.

		@TODO Bug: If there is the current human's cat in the station and other cats
		too, the other humans will not be able to reach the station because it
		will be closed.
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
			# Another human's cat is found, notify the owner if he/she is not
			# in the same station as the current human
			elif human.stationId != toContact.stationId:
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
		'''
		Method to run the simulation of one step. Returns either
		simulator.STATE_ALL_CATS_FOUND or simulator.STATE_CATS_MISSING depending
		on the number of remaining/reachable cats.

		It first updates the position of every remaining cats.
		Then for each human, checks if there is a cat where they are (the cat
		can have moved there in this step), then update the humans' positions
		and then recheck for cats.
		'''

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
			human.update(self._getNeighbourNodes(human.stationId))
			# Check to know if there are any cats where the human arrived
			self._checkNodeForCats(human)
			if human.isLookingForCat() or human.hasLastPosition():
				nbRemainingHumans += 1

		# Update turn number
		self.turn += 1

		if nbRemainingHumans == 0:
			return simulator.STATE_ALL_CATS_FOUND

		return simulator.STATE_CATS_MISSING

	def mainLoop(self):
		'''
		Method to run a whole simulation at once (instead of manually  step by
		step). It will run every steps until config.max_turns are reached or
		every cats are found.
		'''

		result = simulator.STATE_CATS_MISSING
		while len(self.cats) > 0 and self.turn < config.max_turns\
			and result == simulator.STATE_CATS_MISSING:
			result = self.step()

		self.sendReport()

	def sendReport(self):
		'''
		Method to call ideally after the end of the simulation to get different
		information about how it went. All the information are sent to the
		messenger.
		'''

		totalHumanTurns = 0
		for h in self.humans:
			message = ''
			if self.humans[h].isLookingForCat():
				message = '{} is still looking'
				data = [h]
			elif self.humans[h].cantReachCat():
				message = '{} can not reach cat'
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
		'''
		Method to send a message to the messenger, taking in account of if the
		message must always be sent or only on verbose mode.
		'''

		isVerboseLevelOk = self.verbose and onlyVerbose or not onlyVerbose
		if data:
			message = message.format(*data)

		if isVerboseLevelOk and self.messenger is not None:
			self.messenger.send(message)
