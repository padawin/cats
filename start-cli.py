#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
from argparse import ArgumentParser

from simulator import simulator
from city import underground
import config
import util


def main(argv):
	parser = ArgumentParser()

	parser.add_argument(
		"-v", "--verbose",
		dest="verbose", help="Enable verbose mode", action="store_true"
	)
	parser.add_argument(
		"-p", "--population",
		dest="population",
		help="Number of cats/owners to spawn",
		metavar="POPULATION"
	)

	args = parser.parse_args()
	population = int(args.population)
	verbose = args.verbose

	stations = util.readCSVFile(config.stationsFixture)
	connections = util.readCSVFile(config.connectionsFixture)
	network = underground.network(list(stations), list(connections))
	s = simulator(network, verbose)
	s.initialiseActors(population)
	s.mainLoop()

if __name__ == "__main__":
	main(sys.argv[1:])
