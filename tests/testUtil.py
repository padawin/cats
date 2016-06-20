# -*- coding: utf-8 -*-
import unittest
from collections import OrderedDict

import tests.common
import util


class utilTests(tests.common.common):
	def test_read_unexisting_csv_file(self):
		with self.assertRaises(FileNotFoundError):
			util.readCSVFile('foo.csv')

	def test_valid_csv(self):
		data = util.readCSVFile('data-tests/valid.csv')
		self.assertEquals([['foo', 'bar', 'toto'], ['test', 'there', 'here']], data)

	def test_empty_csv(self):
		data = util.readCSVFile('data-tests/empty.csv')
		self.assertEquals([], data)
