import time
import numpy as np

class Shutter:
	def __init__(self, mainInst):
		self.mainInst = mainInst

		self.value = 0
		self.max_value = 30		# Zeit in sekunden von ganz geschlossen bis ganz offen
		self.state = 0			# 0: steht still, 1: geht hoch, 2: geht runter
		self.relay_states = np.array([False, False])	# True wenn Relais geschaltet werden soll
											# stop: [False, False], hoch: [True, False], runter: [False, True]

		self.starttime_of_movement = -1

	def shutter_up(self):
		# TODO Timing with Schedule Module
		self.shutter_stop()

		self.state = 1
		self.starttime_of_movement = time.time()

		self.relay_states = np.array([True, False])
		self.set_arduino_mask()

	def shutter_down(self):
		# TODO Timing with Schedule Module
		self.shutter_stop()

		self.state = 2
		self.starttime_of_movement = time.time()

		self.relay_states = np.array([False, True])
		self.set_arduino_mask()

	def shutter_stop(self):
		# Update Intern values
		if self.starttime_of_movement != -1:
			if self.state == 1:		# Wenn Rolladen hoch ging, Zeit addieren
				self.value += time.time() - self.starttime_of_movement
			elif self.state == 2:	# Wenn Rolladen runter ging, Zeit abziehen
				self.value -= time.time() - self.starttime_of_movement

			# Keep value in ranges
			if self.value > self.max_value:
				self.value = self.max_value
			elif self.value < 0:
				self.value = 0

		self.starttime_of_movement = -1
		self.state = 0

		# Send values to Arduino
		self.relay_states = np.array([False, False])
		self.set_arduino_mask()

	def set_arduino_mask(self):
		idx = self.mainInst.Arduino.mask_idx_shutter
		self.mainInst.Arduino.values_to_send_mask[idx:] = True