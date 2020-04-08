import numpy as np

class WC:
	# WC: WarmCold white
	def __init__(self, mainInst):
		self.mainInst = mainInst
		self.wcm_values = np.array([255, 255, 0])
		self.relay_value = False
		self.btn_relay_value = False

	def set_relay_value(self):
		self.relay_value = np.any((self.wcm_values[:2] * self.wcm_values[2]/255 > 0))

	def relay_btn(self):
		self.btn_relay_value = not self.btn_relay_value
		self.set_arduino_mask()

	def balance_to_values(self, balance):
		self.wcm_values[0] = 255 + balance if balance < 0 else 255
		self.wcm_values[1] = 255 - balance if balance > 0 else 255

		self.set_relay_value()
		self.set_arduino_mask()

	def brightness_to_value(self, brightness):
		self.wcm_values[2] = brightness

		self.set_relay_value()

		self.set_arduino_mask()


	### Utils ###
	def set_arduino_mask(self):
		idx_color = self.mainInst.Arduino.mask_idx_wc
		self.mainInst.Arduino.values_to_send_mask[idx_color: idx_color+2] = True

		idx_relay = self.mainInst.Arduino.mask_idx_wcrls
		self.mainInst.Arduino.values_to_send_mask[idx_relay: idx_relay+2] = True
