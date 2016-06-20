# -*- coding: utf-8 -*-

import random

from population import actor
from city import underground
import config
import util


class simulator(object):
	def __init__(self, actorsNumber):
		self._initialiseCityUndergroundNetwork()
		self._initialiseActors(actorsNumber)

	def _initialiseCityUndergroundNetwork(self):
		stations = util.readCSVFile(config.stationsFixture)
		connections = util.readCSVFile(config.connectionsFixture)
		self.cityUndergroundNetwork = underground.network(
			list(stations),
			list(connections)
		)

	def _initialiseActors(self, actorsNumber):
		positionActors = [
			# Takes 2 different values from the keys of the graph's nodes
			# each value will be the position of the cat and of the owner
			random.sample(self.cityUndergroundNetwork.getStationKeys(), 2)
			# this repeated as many times as we have actors
			for _ in range(actorsNumber)
		]

		self.cats = []
		self.humans = []
		for index, stationIds in enumerate(positionActors):
			self.humans.append(simulator._createHuman(index, stationIds[0]))
			self.cats.append(simulator._createCat(index, stationIds[1]))

	def _createHuman(idHuman, stationId):
		human = actor.human(idHuman)
		human.setStationId(stationId)
		return human

	def _createCat(idCat, stationId):
		cat = actor.cat(idCat)
		cat.setStationId(stationId)
		return cat
