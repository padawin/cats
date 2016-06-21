#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
from argparse import ArgumentParser

from src.simulator import simulator
from src.city import underground
from src import config
from src import util


class messenger(object):
	def send(self, message):
		print(message)


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
		metavar="POPULATION",
		type=int
	)

	args = parser.parse_args()

	if args.population is None:
		raise ValueError('The population is supposed to be an integer')

	population = args.population
	verbose = args.verbose

	stations = util.readCSVFile(config.stationsFixture)
	connections = util.readCSVFile(config.connectionsFixture)
	network = underground.network(list(stations), list(connections))
	s = simulator(network, messenger=messenger(), verbose=verbose)
	s.initialiseActors(population)
	s.mainLoop()

if __name__ == "__main__":
	main(sys.argv[1:])
