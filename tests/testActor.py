# -*- coding: utf-8 -*-
import unittest

from src import actor
import tests.common
from collections import OrderedDict


class actorTests(tests.common.common):
	'''
	Class to test the actor class
	'''

	def test_set_station_actor(self):
		'''
		Test the process to set an actor's station
		'''
		a = actor.actor(1)
		a.setStationId(10)
		self.assertEquals(a.stationId, 10)

	def test_set_station_cat(self):
		'''
		Test the process to set a cat's station, it is the same as for the
		actor.
		'''
		a = actor.cat(1)
		a.setStationId(10)
		self.assertEquals(a.stationId, 10)

	def test_set_station_human(self):
		'''
		Test the process to set a human's station. When changing a human's
		station, the human saves the last station he visited.
		'''
		a = actor.human(1)
		a.setStationId(10)
		self.assertEquals(a.lastVisitedStation, None)
		self.assertEquals(a.stationId, 10)
		a.setStationId(11)
		self.assertEquals(a.lastVisitedStation, 10)
		self.assertEquals(a.stationId, 11)

	def test_choose_station_actor(self):
		'''
		An actor can't choose a station, only children classes of actor can.
		'''
		a = actor.actor(1)
		with self.assertRaises(NotImplementedError):
			a.chooseStationId([1, 2, 3])

	def test_choose_station_cat(self):
		'''
		When a cat choose a station from a list of stations, it is regardless
		of where he went before.
		'''
		a = actor.cat(1)
		a.setStationId(1)
		result = a.chooseStationId([1, 2, 3])
		self.assertIn(a.stationId, [1, 2, 3])
		self.assertEquals(result, True)

	def test_choose_station_no_choice_cat(self):
		'''
		Suggesting to a cat to choose a station among an empty list does not
		change its current station
		'''
		a = actor.cat(1)
		a.setStationId(1)
		result = a.chooseStationId([])
		self.assertEquals(a.stationId, 1)
		self.assertEquals(result, False)

	def test_choose_station_human(self):
		'''
		If possible, a human chooses only a station different to the one he was
		just before
		'''
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
		'''
		Suggesting to a human to choose a station among an empty list does not
		change its current station
		'''
		a = actor.human(1)
		a.setStationId(2)
		result = a.chooseStationId([])
		self.assertEquals(result, False)
		self.assertEquals(a.stationId, 2)

	def test_human_is_looking_for_cat(self):
		'''
		State test for the human. Once the cat is retrieved, the human is not
		looking for it anymore.
		'''
		h = actor.human(1)
		self.assertEquals(h.isLookingForCat(), True)
		h.catRetrieved()
		self.assertEquals(h.isLookingForCat(), False)

	def test_human_catFoundAt(self):
		'''
		Once a human heard his cat has been seen, he is not looking for it any
		more (but heads towards it instead) and saves the station id where the
		cat has been spotted.
		'''
		h = actor.human(1)
		self.assertEquals(h.isLookingForCat(), True)
		h.catFoundAt(10)
		self.assertEquals(h.isLookingForCat(), False)
		self.assertEquals(h.targetStation, 10)

	def test_human_hasLastPosition(self):
		'''
		When the cat is spotted, the human has its last position.
		'''
		h = actor.human(1)
		self.assertEquals(h.hasLastPosition(), False)
		h.catFoundAt(10)
		self.assertEquals(h.hasLastPosition(), True)
		self.assertEquals(h.targetStation, 10)

	def test_update_cat(self):
		'''
		Test to update the cat's. It will change its position only on odd turns
		'''
		c = actor.cat(1)
		c.setStationId(1)
		c.update(1, [2])
		self.assertEquals(c.stationId, 2)
		c.update(2, [3])
		self.assertEquals(c.stationId, 2)

	def test_update_human(self):
		'''
		Test to update the human. It is incomplete and does not test the path
		finding. Also did not set the network to the human
		'''
		# @TODO Incomplete test, needs a grid to properly work
		h = actor.human(1)
		h.setStationId(1)
		h.update([2])
		self.assertEquals(h.stationId, 2)
