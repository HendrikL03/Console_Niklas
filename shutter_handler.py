

class Shutter:
	def __init__(self, mainInst):
		self.mainInst = mainInst

		self.value = 0
		self.max_value = 30		# Zeit in sekunden von ganz geschlossen bis ganz offen
		self.state = 0			# 0: steht still, 1: geht hoch, 2: geht runter
		self.relay_states = [False, False]	# True wenn Relais geschaltet werden soll
											# stop: [False, False], hoch: [True, False], runter: [False, True]

	def shutter_up(self):
		self.relay_states = [True, False]
		self.set_arduino_mask()

	def shutter_down(self):
		self.relay_states = [False, True]
		self.set_arduino_mask()

	def shutter_stop(self):
		self.relay_states = [False, False]
		self.set_arduino_mask()

	def set_arduino_mask(self):
		idx = self.mainInst.Arduino.mask_idx_shutter
		self.mainInst.Arduino.values_to_send_mask[idx:] = True