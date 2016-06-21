# -*- coding: utf-8 -*-
import csv


def readCSVFile(file):
	f = open(file)
	csvReader = csv.reader(f)

	rows = []
	for row in csvReader:
		rows.append(row)

	return rows
