# -*- coding: utf-8 -*-
import unittest

from population import actor
import tests.common
from collections import OrderedDict


class actorTests(tests.common.common):
	def test_set_station_actor(self):
		a = actor.actor()
		a.setStationId(10)
		self.assertEquals(a.stationId, 10)

	def test_set_station_cat(self):
		a = actor.cat()
		a.setStationId(10)
		self.assertEquals(a.stationId, 10)

	def test_set_station_human(self):
		a = actor.human()
		a.setStationId(10)
		self.assertEquals(a.lastVisitedStation, None)
		self.assertEquals(a.stationId, 10)
		a.setStationId(11)
		self.assertEquals(a.lastVisitedStation, 10)
		self.assertEquals(a.stationId, 11)
