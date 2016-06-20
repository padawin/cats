# -*- coding: utf-8 -*-
import unittest

from population import actor
import tests.common
from collections import OrderedDict


class actorTests(tests.common.common):
	def test_set_station_actor(self):
		a = actor.actor(1)
		a.setStationId(10)
		self.assertEquals(a.stationId, 10)

	def test_set_station_cat(self):
		a = actor.cat(1)
		a.setStationId(10)
		self.assertEquals(a.stationId, 10)

	def test_set_station_human(self):
		a = actor.human(1)
		a.setStationId(10)
		self.assertEquals(a.lastVisitedStation, None)
		self.assertEquals(a.stationId, 10)
		a.setStationId(11)
		self.assertEquals(a.lastVisitedStation, 10)
		self.assertEquals(a.stationId, 11)

	def test_choose_station_actor(self):
		a = actor.actor(1)
		with self.assertRaises(NotImplementedError):
			a.chooseStationId([1, 2, 3])

	def test_choose_station_cat(self):
		a = actor.cat(1)
		a.chooseStationId([1, 2, 3])
		self.assertIn(a.stationId, [1, 2, 3])

	def test_choose_station_human(self):
		a = actor.human(1)
		a.setStationId(1)
		a.setStationId(42)
		a.chooseStationId([1, 2, 3])
		self.assertIn(a.stationId, [2, 3])

	def test_comparison_cat_human_ids(self):
		c1 = actor.cat(1)
		c2 = actor.cat(2)
		h = actor.human(1)
		self.assertTrue(h.isItMyCat(c1.id))
		self.assertFalse(h.isItMyCat(c2.id))
