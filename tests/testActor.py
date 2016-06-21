# -*- coding: utf-8 -*-
import unittest

from src import actor
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
		result = a.chooseStationId([1, 2, 3])
		self.assertIn(a.stationId, [1, 2, 3])
		self.assertEquals(result, True)

	def test_choose_station_no_choice_cat(self):
		a = actor.cat(1)
		result = a.chooseStationId([])
		self.assertEquals(a.stationId, None)
		self.assertEquals(result, False)

	def test_choose_station_human(self):
		a = actor.human(1)
		self.assertEquals(a.lastVisitedStation, None)
		a.setStationId(1)
		self.assertEquals(a.lastVisitedStation, None)
		a.setStationId(42)
		self.assertEquals(a.lastVisitedStation, 1)
		a.chooseStationId([1, 2, 3])
		self.assertIn(a.stationId, [2, 3])
		self.assertEquals(a.lastVisitedStation, 42)

	def test_choose_station_human_one_choice(self):
		'''
		situation of dead end:
		The human goes from 1 to 2, then from 2 can only go back to 1,
		he then must
		'''
		a = actor.human(1)
		a.setStationId(2)
		self.assertEquals(a.stationId, 2)
		result = a.chooseStationId([1])
		self.assertEquals(result, True)
		self.assertEquals(a.stationId, 1)
		self.assertEquals(a.lastVisitedStation, 2)
		result = a.chooseStationId([2])
		self.assertEquals(result, True)
		self.assertEquals(a.stationId, 2)

	def test_choose_station_human_no_choice(self):
		a = actor.human(1)
		a.setStationId(2)
		result = a.chooseStationId([])
		self.assertEquals(result, False)
		self.assertEquals(a.stationId, 2)

	def test_comparison_cat_human_ids(self):
		c1 = actor.cat(1)
		c2 = actor.cat(2)
		h = actor.human(1)
		self.assertTrue(h.id == c1.id)
		self.assertFalse(h.id == c2.id)

	def test_human_is_looking_for_cat(self):
		h = actor.human(1)
		c = actor.cat(1)
		self.assertEquals(h.isLookingForCat(), True)
		h.catRetrieved()
		self.assertEquals(h.isLookingForCat(), False)

	def test_human_catFoundAt(self):
		h = actor.human(1)
		self.assertEquals(h.isLookingForCat(), True)
		h.catFoundAt(10)
		self.assertEquals(h.isLookingForCat(), False)
		self.assertEquals(h.targetStation, 10)

	def test_human_hasLastPosition(self):
		h = actor.human(1)
		self.assertEquals(h.hasLastPosition(), False)
		h.catFoundAt(10)
		self.assertEquals(h.hasLastPosition(), True)
		self.assertEquals(h.targetStation, 10)

	def test_update_cat(self):
		c = actor.cat(1)
		c.setStationId(1)
		c.update(1, [2])
		self.assertEquals(c.stationId, 2)
		c.update(2, [3])
		self.assertEquals(c.stationId, 2)

	def test_update_human(self):
		# @TODO Incomplete test, needs a grid to properly work
		h = actor.human(1)
		h.setStationId(1)
		h.update([2])
		self.assertEquals(h.stationId, 2)
