# -*- coding: utf-8 -*-
import unittest

from city import underground
import tests.common
from collections import OrderedDict


class networkTests(tests.common.common):
	def test_invalid_stations(self):
		londonStations = 'foo'
		with self.assertRaises(ValueError):
			underground.network(londonStations, None)

	def test_invalid_connections(self):
		londonConnections = 'foo'
		with self.assertRaises(ValueError):
			underground.network([], londonConnections)

	def test_underground_generation(self):
		london = self.prepareLondon()
		# test some random entries
		self.assertEquals(
			london.stations['277'],
			{'name': 'Warren Street', 'connections': ['89', '102', '89', '192']}
		)
		self.assertEquals(
			london.stations['1'],
			{'name': 'Acton Town', 'connections': ['52', '73', '73', '234', '265']}
		)
		self.assertEquals(
			london.stations['31'],
			{'name': 'Bounds Green', 'connections': ['9', '303']}
		)
		self.assertEquals(
			london.stations['127'],
			{'name': 'Holland Park', 'connections': ['186', '226']}
		)
		self.assertEquals(
			london.stations['42'],
			{'name': 'Canary Wharf', 'connections': ['120', '292', '41', '183']}
		)
		self.assertEquals(
			london.stations['146'],
			{'name': 'Knightsbridge', 'connections': ['133', '236']}
		)

		self.assertEquals(len(london.stations), 302)
