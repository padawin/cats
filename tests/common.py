# -*- coding: utf-8 -*-
from __future__ import absolute_import
import unittest

import config
import util
from city import underground


class common(unittest.TestCase):
	def setUp(self):
		pass

	def prepareLondon(self):
		londonStations = util.readCSVFile(config.stationsFixture)
		londonConnections = util.readCSVFile(config.connectionsFixture)
		london = underground.network(
			list(londonStations),
			list(londonConnections)
		)
		return london
