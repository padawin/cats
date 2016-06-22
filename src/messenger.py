# -*- coding: utf-8 -*-


class messenger(object):
	def send(self, message):
		typeMessage = type(message)
		if typeMessage is dict:
			print(self.formatMessage(message))
		else:
			raise ValueError(
				'Invalid message, dict expected, {} provided'.format(
					typeMessage
				)
			)

	def formatMessage(self, message):
		if 'type' not in message:
			return message
		else:
			return self.getTemplate(message['type']).format(**message)

	def getTemplate(self, typeMessage):
		templates = {
			'CAT_RETRIEVED':
				'Owner {human_id} found cat {cat_id} - {station} is now closed.',
			'CAT_SPOTTED': '{spotted_by} saw cat {cat_id} at {station_spotted}',
			'STILL_LOOKING': '{human_id} is still looking',
			'CANT_REACH_CAT': '{human_id} can not reach cat',
			'HUMAN_SUM_UP': '{human_id} found cat in {nb_turns} turns',
			'REPORT': 'Simulation finished after {turns} turns\n' +
				'Total number of cats/humans: {population_size}\n' +
				'Number of cats found: {cats_found}\n' +
				'Average number of movements required to find a cat: ' +
				'{average_time_to_find_cat}'

		}

		if typeMessage not in templates:
			raise ValueError('Invalid message type {}'.format(typeMessage))

		return templates[typeMessage]
