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
			{
				'name': 'Warren Street',
				'status': underground.network.STATION_OPEN,
				'connections': ['89', '102', '89', '192'],
				'closedConnections': []
			}
		)
		self.assertEquals(
			london.stations['1'],
			{
				'name': 'Acton Town',
				'status': underground.network.STATION_OPEN,
				'connections': ['52', '73', '73', '234', '265'],
				'closedConnections': []
			}
		)
		self.assertEquals(
			london.stations['31'],
			{
				'name': 'Bounds Green',
				'status': underground.network.STATION_OPEN,
				'connections': ['9', '303'],
				'closedConnections': []
			}
		)
		self.assertEquals(
			london.stations['127'],
			{
				'name': 'Holland Park',
				'status': underground.network.STATION_OPEN,
				'connections': ['186', '226'],
				'closedConnections': []
			}
		)
		self.assertEquals(
			london.stations['42'],
			{
				'name': 'Canary Wharf',
				'status': underground.network.STATION_OPEN,
				'connections': ['120', '292', '41', '183'],
				'closedConnections': []
			}
		)
		self.assertEquals(
			london.stations['146'],
			{
				'name': 'Knightsbridge',
				'status': underground.network.STATION_OPEN,
				'connections': ['133', '236'],
				'closedConnections': []
			}
		)

		self.assertEquals(len(london.stations), 302)

	def test_close_stations_invalid_station(self):
		london = self.prepareLondon()
		with self.assertRaises(ValueError) as error:
			london.closeStation('foobar')
		self.assertEquals(str(error.exception), 'Invalid station "foobar"')

	def test_close_stations(self):
		london = self.prepareLondon()
		london.closeStation(42)

		self.assertEquals(
			london.stations['42'],
			{
				'name': 'Canary Wharf',
				'status': underground.network.STATION_CLOSED,
				'connections': ['120', '292', '41', '183'],
				'closedConnections': []
			}
		)
		self.assertEquals(london.stations['120']['connections'], ['238'])
		self.assertEquals(london.stations['120']['closedConnections'], ['42'])

		self.assertEquals(
			london.stations['292']['connections'],
			['201', '284']
		)
		self.assertEquals(london.stations['292']['closedConnections'], ['42'])

		self.assertEquals(
			london.stations['41']['connections'],
			['216', '253', '23']
		)
		self.assertEquals(london.stations['41']['closedConnections'], ['42'])

		self.assertEquals(london.stations['183']['connections'], ['43'])
		self.assertEquals(london.stations['183']['closedConnections'], ['42'])
