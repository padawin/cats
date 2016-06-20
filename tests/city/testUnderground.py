# -*- coding: utf-8 -*-
import unittest

import config
import util
from city import underground
import tests.common
from collections import OrderedDict


class networkTests(tests.common.common):
	def test_invalid_stations(self):
		londonStations = 'foo'
		with self.assertRaises(ValueError):
			underground.network(londonStations, None)

	def test_station_generation(self):
		londonStations = util.readCSVFile(config.stationsFixture)
		london = underground.network(londonStations)
		# test some random entries
		self.assertEquals(
			london.stations['277'],
			{'name': 'Warren Street', 'connections': []}
		)
		self.assertEquals(
			london.stations['1'],
			{'name': 'Acton Town', 'connections': []}
		)
		self.assertEquals(
			london.stations['31'],
			{'name': 'Bounds Green', 'connections': []}
		)
		self.assertEquals(
			london.stations['127'],
			{'name': 'Holland Park', 'connections': []}
		)
		self.assertEquals(
			london.stations['42'],
			{'name': 'Canary Wharf', 'connections': []}
		)
		self.assertEquals(
			london.stations['146'],
			{'name': 'Knightsbridge', 'connections': []}
		)

		self.assertEquals(len(london.stations), 302)
