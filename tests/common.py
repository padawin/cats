# -*- coding: utf-8 -*-
from __future__ import absolute_import
import unittest

from src import config
from src import util
from src.city import underground


class common(unittest.TestCase):
	def prepareLondon(self):
		londonStations = util.readCSVFile(config.stationsFixture)
		londonConnections = util.readCSVFile(config.connectionsFixture)
		london = underground.network(
			list(londonStations),
			list(londonConnections)
		)
		return london
