#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
from argparse import ArgumentParser

from src.simulator import simulator
from src.city import underground
from src import config
from src import util
from src.messenger import messenger


def main(argv):
	parser = ArgumentParser()

	parser.add_argument(
		"-v", "--verbose",
		dest="verbose", help="Enable verbose mode", action="store_true"
	)
	parser.add_argument(
		"-H", "--human-friendly",
		dest="humanFriendly",
		help="Display the messages as text and not as data",
		action="store_true"
	)
	parser.add_argument(
		"-p", "--population",
		required=True,
		dest="population",
		help="Number of cats/owners to spawn",
		metavar="POPULATION",
		type=int
	)

	args = parser.parse_args()

	population = args.population
	verbose = args.verbose
	humanFriendly = args.humanFriendly

	stations = util.readCSVFile(config.stationsFixture)
	connections = util.readCSVFile(config.connectionsFixture)
	network = underground.network(list(stations), list(connections))
	s = simulator(network, messenger=messenger(humanFriendly), verbose=verbose)
	s.initialiseActors(population)
	s.mainLoop()

if __name__ == "__main__":
	main(sys.argv[1:])
